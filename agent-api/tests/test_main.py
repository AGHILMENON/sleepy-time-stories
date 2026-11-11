from fastapi.testclient import TestClient

from app.llm import FakeLLM
from app.main import app, get_llm

client = TestClient(app)

VALID = {"age_band": "5-6", "hero": "owl", "place": "forest", "minutes": 5}


def use_fake(responses):
    """Make the app use FakeLLM with these queued answers."""
    fake = FakeLLM(responses)
    app.dependency_overrides[get_llm] = lambda: fake
    return fake


def teardown_function():
    app.dependency_overrides.clear()     # reset after every test


def test_health():
    assert client.get("/healthz").json() == {"ok": True}


def test_story_ok():
    use_fake([{"title": "Ollie", "story": "The owl yawned. Goodnight, {CHILD}.", "music_mood": "night"}])
    r = client.post("/stories", json=VALID)
    assert r.status_code == 200
    body = r.json()
    assert "{CHILD}" in body["text"]
    assert body["target_words"] == 550
    assert body["word_count"] == 5


def test_child_name_rejected():
    use_fake([])
    r = client.post("/stories", json={**VALID, "child_name": "Meera"})
    assert r.status_code == 422


def test_bad_mood_falls_back_to_night():
    use_fake([{"title": "Ollie", "story": "Soft and sleepy.", "music_mood": "thunderstorm"}])
    assert client.post("/stories", json=VALID).json()["music_mood"] == "night"


def test_empty_story_gives_502():
    use_fake([{"title": "Ollie", "story": ""}])
    assert client.post("/stories", json=VALID).status_code == 502


def test_child_name_never_reaches_the_ai():
    fake = use_fake([{"title": "Ollie", "story": "Sleepy owl.", "music_mood": "night"}])
    client.post("/stories", json=VALID)
    system_prompt, user_prompt = fake.calls[0]
    assert "{CHILD}" in system_prompt          # the AI only ever sees the placeholder