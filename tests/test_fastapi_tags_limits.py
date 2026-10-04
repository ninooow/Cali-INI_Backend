import pytest
from datetime import datetime, timezone
from fastapi.testclient import TestClient

from fastapi_app import app
from database import SessionLocal, init_db
from models.core import Asset, SensorTag, EquipmentLimit

client = TestClient(app)

@pytest.fixture(scope="function")
def db_session():
    init_db()
    session = SessionLocal()
    yield session
    session.close()

def create_sample_tags_and_limits(session):
    asset1 = Asset(
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
    asset2 = Asset(
        tag_number="TEST-COMP-01",
        asset_name="Test Compressor 01",
        plant_code="PL01",
        equipment_type="Compressor",
        equipment_class="Rotary",
        discipline="Mechanical",
        criticality="MEDIUM",
        core_mode="hourly",
        fla_amp=250.0,
        is_active=True,
    )
    session.add_all([asset1, asset2])
    session.commit()
    session.refresh(asset1)
    session.refresh(asset2)

    # Sensor tags
    tag1 = SensorTag(
        asset_id=asset1.asset_id,
        pi_tag="31PM01A_VIB",
        canonical_param="VIB",
        name="Vibration Inboard",
        description="Overall velocity RMS",
        engineering_unit="mm/s",
        span=25.0,
        typical_value=2.5,
        zero_value=0.0,
        instrument_tag="VT-3101A",
        is_active=True,
    )
    tag2 = SensorTag(
        asset_id=asset2.asset_id,
        pi_tag="42K01_TEMP",
        canonical_param="TEMP",
        name="Suction Temp",
        engineering_unit="degC",
        is_active=True,
    )
    session.add_all([tag1, tag2])

    # Equipment limits
    lim1 = EquipmentLimit(
        asset_id=asset1.asset_id,
        parameter="VIB",
        unit="mm/s",
        alarm_limit=4.5,
        trip_limit=7.1,
    )
    lim2 = EquipmentLimit(
        asset_id=asset2.asset_id,
        parameter="TEMP",
        unit="degC",
        alarm_limit=85.0,
        trip_limit=95.0,
    )
    session.add_all([lim1, lim2])
    session.commit()

    return {"asset1": asset1, "asset2": asset2}


def test_sensor_tags_endpoints(db_session):
    seed = create_sample_tags_and_limits(db_session)
    aid1 = seed["asset1"].asset_id
    aid2 = seed["asset2"].asset_id

    # 1. Global list
    resp = client.get("/api/v1/sensor-tags")
    assert resp.status_code == 200
    tags = resp.json()["data"]
    assert len(tags) == 2

    # 2. Filter by asset_id
    resp = client.get(f"/api/v1/sensor-tags?asset_id={aid1}")
    assert resp.status_code == 200
    tags1 = resp.json()["data"]
    assert len(tags1) == 1
    assert tags1[0]["pi_tag"] == "31PM01A_VIB"
    assert tags1[0]["instrument_tag"] == "VT-3101A"

    # 3. Filter by canonical_param
    resp = client.get("/api/v1/sensor-tags?canonical_param=TEMP")
    assert resp.status_code == 200
    assert len(resp.json()["data"]) == 1
    assert resp.json()["data"][0]["canonical_param"] == "TEMP"

    # 4. Nested /assets/{id}/tags
    resp = client.get(f"/api/v1/assets/{aid2}/tags")
    assert resp.status_code == 200
    assert len(resp.json()["data"]) == 1
    assert resp.json()["data"][0]["pi_tag"] == "42K01_TEMP"

    # 5. Nested with non-existent asset -> 404
    resp = client.get("/api/v1/assets/9999/tags")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Asset not found"


def test_equipment_limits_endpoints(db_session):
    seed = create_sample_tags_and_limits(db_session)
    aid1 = seed["asset1"].asset_id
    aid2 = seed["asset2"].asset_id

    # 1. Global list
    resp = client.get("/api/v1/equipment-limits")
    assert resp.status_code == 200
    limits = resp.json()["data"]
    assert len(limits) == 2

    # 2. Filter by asset_id
    resp = client.get(f"/api/v1/equipment-limits?asset_id={aid1}")
    assert resp.status_code == 200
    limits1 = resp.json()["data"]
    assert len(limits1) == 1
    assert limits1[0]["parameter"] == "VIB"
    assert limits1[0]["alarm_limit"] == 4.5
    assert limits1[0]["trip_limit"] == 7.1

    # 3. Filter by parameter
    resp = client.get("/api/v1/equipment-limits?parameter=TEMP")
    assert resp.status_code == 200
    assert len(resp.json()["data"]) == 1
    assert resp.json()["data"][0]["parameter"] == "TEMP"

    # 4. Nested /assets/{id}/limits
    resp = client.get(f"/api/v1/assets/{aid2}/limits")
    assert resp.status_code == 200
    assert len(resp.json()["data"]) == 1
    assert resp.json()["data"][0]["trip_limit"] == 95.0

    # 5. Nested with non-existent asset -> 404
    resp = client.get("/api/v1/assets/9999/limits")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Asset not found"
