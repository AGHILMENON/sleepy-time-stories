from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    assert client.get("/healthz").json() == {"ok": True}

def test_story_ok():
    r = client.post("/stories", json={"age_band": "5-6", "hero": "owl", "place": "forest", "minutes": 10})
    assert r.status_code == 200
    assert "{CHILD}" in r.json()["text"]

def test_child_name_rejected():
    r = client.post("/stories", json={"age_band": "5-6", "hero": "owl", "place": "forest", "minutes": 10, "child_name": "Meera"})
    assert r.status_code == 422