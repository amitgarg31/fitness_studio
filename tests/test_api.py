import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from app.main import app
from app.db import engine, init_db
from app.models import FitnessClass
from app.seed import run as seed_run

client = TestClient(app)

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    init_db()
    seed_run()
    yield

def test_list_classes_ok():
    r = client.get("/classes?tz=Asia/Kolkata")
    assert r.status_code == 200
    data = r.json()["classes"]
    assert len(data) >= 1
    assert "available_slots" in data[0]

def test_book_ok_and_no_slots():
    r = client.get("/classes")
    cid = r.json()["classes"][0]["id"]

    r = client.post("/book", json={
        "class_id": cid,
        "client_name": "Amit",
        "client_email": "amit@example.com"
    })
    assert r.status_code == 200
    booking = r.json()
    assert booking["class_id"] == cid

def test_bookings_by_email():
    r = client.get("/bookings", params={"email": "amit@example.com"})
    assert r.status_code == 200
    assert len(r.json()["bookings"]) >= 1
