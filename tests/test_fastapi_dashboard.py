import pytest
from datetime import datetime, timezone
from fastapi.testclient import TestClient

from fastapi_app import app
from database import SessionLocal, init_db
from models.core import Asset
from models.telemetry import HourlyMeasurement
from models.workflow import ProblemTicket
from models.analytics import AnalysisRun

client = TestClient(app)

@pytest.fixture(scope="function")
def db_session():
    init_db()
    session = SessionLocal()
    yield session
    session.close()

def test_dashboard_endpoint_empty_db(db_session):
    resp = client.get("/api/v1/analytics/dashboard")
    assert resp.status_code == 200
    data = resp.json()
    assert data["header"]["scope"] == "All assets"
    assert data["header"]["data_status"] == "UNKNOWN"
    assert data["header"]["as_of"] is None
    assert data["attention_summary"] == {"total": 0, "p1": 0, "p2": 0, "p3": 0, "p4": 0}
    assert data["attention_items"] == []
    assert data["active_assets_count"] == 0

def test_dashboard_endpoint_with_data(db_session):
    asset = Asset(
        tag_number="31-PM-01A",
        asset_name="Quench Water Pump A",
        plant_code="PL01",
        equipment_type="Pump",
        equipment_class="Rotary",
        discipline="Mechanical",
        criticality="HIGH",
        core_mode="hourly",
        is_active=True,
    )
    db_session.add(asset)
    db_session.commit()
    db_session.refresh(asset)

    now = datetime.now(timezone.utc)

    run = AnalysisRun(
        started_at=now,
        completed_at=now,
        reference_time=now,
        engine_version="V11.x",
        runtime_mode="SNAPSHOT",
        status="COMPLETED",
    )
    db_session.add(run)

    ticket1 = ProblemTicket(
        ticket_id="TICKET-001",
        asset_id=asset.asset_id,
        opened_at=now,
        condition_state="ANOMALY",
        priority="P1",
        owner_role="Operator",
        ticket_state="OPEN",
        action_status="NOT_STARTED",
    )
    ticket2 = ProblemTicket(
        ticket_id="TICKET-002",
        asset_id=asset.asset_id,
        opened_at=now,
        condition_state="WARNING",
        priority="P2",
        owner_role="Operator",
        ticket_state="IN_PROGRESS",
        action_status="INVESTIGATING",
    )
    ticket3 = ProblemTicket(
        ticket_id="TICKET-003",
        asset_id=asset.asset_id,
        opened_at=now,
        condition_state="NORMAL",
        priority="P4",
        owner_role="Operator",
        ticket_state="CLOSED",
        action_status="COMPLETED",
    )
    db_session.add_all([ticket1, ticket2, ticket3])
    db_session.commit()

    resp = client.get("/api/v1/analytics/dashboard")
    assert resp.status_code == 200
    data = resp.json()

    assert data["header"]["data_status"] == "PASS"
    assert data["active_assets_count"] == 1
    assert data["attention_summary"]["total"] == 2
    assert data["attention_summary"]["p1"] == 1
    assert data["attention_summary"]["p2"] == 1
    assert data["attention_summary"]["p3"] == 0
    assert data["attention_summary"]["p4"] == 0

    items = data["attention_items"]
    assert len(items) == 2
    t_ids = {t["ticket_id"] for t in items}
    assert t_ids == {"TICKET-001", "TICKET-002"}
