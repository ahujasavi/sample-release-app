import pytest
from src.app import app as flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json["status"] == "ok"


def test_list_inventory(client):
    r = client.get("/inventory")
    assert r.status_code == 200
    assert r.json["count"] == 2


def test_get_existing_item(client):
    r = client.get("/inventory/SKU-001")
    assert r.status_code == 200
    assert r.json["name"] == "Widget A"
    assert "reorder_point" in r.json


def test_get_missing_item(client):
    r = client.get("/inventory/SKU-999")
    assert r.status_code == 404


def test_adjust_qty(client):
    r = client.post("/inventory/SKU-002/adjust", json={"delta": -10})
    assert r.status_code == 200
    assert r.json["new_qty"] == 35


def test_adjust_qty_floor_at_zero(client):
    r = client.post("/inventory/SKU-002/adjust", json={"delta": -9999})
    assert r.json["new_qty"] == 0
