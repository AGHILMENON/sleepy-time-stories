from fastapi.testclient import TestClient

from app.llm import FakeLLM
from app.main import app, get_reviewer, get_writer

client = TestClient(app)

VALID = {"age_band": "5-6", "hero": "owl", "place": "forest", "minutes": 5}
GOOD_550 = " ".join(["The little owl yawned softly by the sea."] * 61)


def draft(text=GOOD_550, mood="night"):
    return {"title": "Ollie", "story": text, "music_mood": mood}


def review(safety="pass", calm=5, age_fit=5, quality=4, fix=""):
    return {"safety": safety, "safety_reasons": [], "calm": calm,
            "age_fit": age_fit, "quality": quality, "fix_notes": fix}


def use_fakes(drafts, reviews):
    writer, reviewer = FakeLLM(drafts), FakeLLM(reviews)
    app.dependency_overrides[get_writer] = lambda: writer
    app.dependency_overrides[get_reviewer] = lambda: reviewer
    return writer, reviewer


def teardown_function():
    app.dependency_overrides.clear()


def test_health():
    assert client.get("/healthz").json() == {"ok": True}


def test_child_name_rejected():
    use_fakes([], [])
    assert client.post("/stories", json={**VALID, "child_name": "Meera"}).status_code == 422


def test_approved_first_try():
    use_fakes([draft()], [review()])
    body = client.post("/stories", json=VALID).json()
    assert body["status"] == "approved"
    assert body["attempts"] == 1


def test_short_story_is_rewritten_with_fix_notes():
    writer, _ = use_fakes([draft("Too short."), draft()], [review(), review()])
    body = client.post("/stories", json=VALID).json()
    assert body["status"] == "approved"
    assert body["attempts"] == 2
    assert "length" in writer.calls[1][1]       # the 2nd request carried the fix notes


def test_fallback_after_three_failures():
    use_fakes([draft()] * 3, [review(safety="fail")] * 3)
    body = client.post("/stories", json=VALID).json()
    assert body["status"] == "fallback_used"
    assert body["title"] == "Tiny Turtle and the Quiet Sea"
    assert len(body["trace"]) == 3


def test_monster_never_reaches_child():
    scary = GOOD_550 + " A monster."
    use_fakes([draft(scary)] * 3, [review()] * 3)     # the AI reviewer wrongly says pass
    body = client.post("/stories", json=VALID).json()
    assert body["status"] == "fallback_used"
    assert "monster" not in body["text"]


def test_child_name_never_reaches_the_ai():
    writer, _ = use_fakes([draft()], [review()])
    client.post("/stories", json=VALID)
    assert "{CHILD}" in writer.calls[0][0]