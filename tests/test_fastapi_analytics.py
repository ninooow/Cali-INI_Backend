import pytest
from datetime import datetime, timezone
from fastapi.testclient import TestClient

from fastapi_app import app
from database import SessionLocal, init_db
from models.core import Asset
from models.analytics import AnalysisRun, ConditionInference, ParameterForecast, RcaMatch

client = TestClient(app)

@pytest.fixture(scope="function")
def db_session():
    init_db()
    session = SessionLocal()
    yield session
    session.close()

def create_sample_analytics_data(session):
    asset = Asset(
        tag_number="TEST-PUMP-01",
        asset_name="Test Pump 01",
        plant_code="PL01",
        equipment_type="Pump",
        equipment_class="Rotary",
        discipline="Mechanical",
        criticality="HIGH",
        core_mode="hourly",
        fla_amp=120.0,
        is_active=True,
    )
    session.add(asset)
    session.commit()
    session.refresh(asset)

    now = datetime.now(timezone.utc)
    run = AnalysisRun(
        started_at=now,
        completed_at=now,
        reference_time=now,
        engine_version="V11.x",
        runtime_mode="SNAPSHOT",
        status="COMPLETED",
    )
    session.add(run)
    session.commit()
    session.refresh(run)

    inf = ConditionInference(
        run_id=run.run_id,
        asset_id=asset.asset_id,
        as_of_time=now,
        overall_state="ANOMALY",
        consequence_class="CRITICAL",
        priority="P1",
        dominant_symptom="Vibration spike on inboard bearing",
        health_index=45.5,
        pca_anomaly_score=3.8,
        max_zscore=4.2,
        statistical_available=True,
    )
    session.add(inf)

    fc = ParameterForecast(
        run_id=run.run_id,
        asset_id=asset.asset_id,
        canonical_param="VIB",
        anchor_time=now,
        target_time=now,
        estimate=5.6,
        lower_bound=4.8,
        upper_bound=6.4,
        source="INFERENCE",
        model_family="Holt-Winters",
        model_type="additive",
        model_quality="GOOD",
        mae=0.12,
        rmse=0.18,
    )
    session.add(fc)

    rca = RcaMatch(
        run_id=run.run_id,
        asset_id=asset.asset_id,
        matched_ar_no="AR-2026-089",
        similarity_score=0.92,
        evidence_strength="STRONG",
        rank_no=1,
        current_supporting_evidence="Vibration amplitude pattern matches bearing wear",
        historical_verified_evidence="Bearing failure verified in 2026 incident",
    )
    session.add(rca)
    session.commit()

    return {"asset": asset, "run": run}


def test_list_analysis_runs_initially_empty(db_session):
    resp = client.get("/api/v1/analytics/runs")
    assert resp.status_code == 200
    assert resp.json()["data"] == []


def test_get_latest_run_404_when_none(db_session):
    resp = client.get("/api/v1/analytics/runs/latest")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "No completed analysis run found"


def test_analytics_endpoints_with_seeded_data(db_session):
    seed = create_sample_analytics_data(db_session)
    run_id = seed["run"].run_id
    asset_id = seed["asset"].asset_id

    # 1. list runs
    resp = client.get("/api/v1/analytics/runs")
    assert resp.status_code == 200
    runs = resp.json()["data"]
    assert len(runs) == 1
    assert runs[0]["run_id"] == run_id
    assert runs[0]["status"] == "COMPLETED"

    # 2. get run detail
    resp = client.get(f"/api/v1/analytics/runs/{run_id}")
    assert resp.status_code == 200
    assert resp.json()["run_id"] == run_id

    # 3. get latest run
    resp = client.get("/api/v1/analytics/runs/latest")
    assert resp.status_code == 200
    assert resp.json()["run_id"] == run_id

    # 4. condition inferences
    resp = client.get(f"/api/v1/analytics/condition-inferences?run_id={run_id}&priority=P1")
    assert resp.status_code == 200
    infs = resp.json()["data"]
    assert len(infs) == 1
    assert infs[0]["priority"] == "P1"
    assert infs[0]["overall_state"] == "ANOMALY"
    assert infs[0]["health_index"] == 45.5

    # 5. parameter forecasts
    resp = client.get(f"/api/v1/analytics/parameter-forecasts?run_id={run_id}&canonical_param=VIB")
    assert resp.status_code == 200
    fcs = resp.json()["data"]
    assert len(fcs) == 1
    assert fcs[0]["canonical_param"] == "VIB"
    assert fcs[0]["estimate"] == 5.6
    assert fcs[0]["model_family"] == "Holt-Winters"

    # 6. rca matches
    resp = client.get(f"/api/v1/analytics/rca-matches?run_id={run_id}&asset_id={asset_id}")
    assert resp.status_code == 200
    rcas = resp.json()["data"]
    assert len(rcas) == 1
    assert rcas[0]["matched_ar_no"] == "AR-2026-089"
    assert rcas[0]["similarity_score"] == 0.92
    assert rcas[0]["evidence_strength"] == "STRONG"
