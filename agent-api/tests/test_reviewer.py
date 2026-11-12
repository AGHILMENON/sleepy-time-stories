from app.llm import FakeLLM
from app.reviewer import review_story

GOOD_550 = " ".join(["The little owl yawned softly by the sea."] * 61)


def ai_says(safety="pass", calm=5, age_fit=5, quality=4, fix=""):
    return {"safety": safety, "safety_reasons": [], "calm": calm,
            "age_fit": age_fit, "quality": quality, "fix_notes": fix}


def test_good_story_is_approved():
    result = review_story(FakeLLM([ai_says()]), GOOD_550, "5-6", 5)
    assert result["approved"] is True


def test_ai_fail_blocks_story():
    result = review_story(FakeLLM([ai_says(safety="fail", fix="Remove the storm.")]), GOOD_550, "5-6", 5)
    assert result["approved"] is False
    assert "Remove the storm." in result["fix_notes"]


def test_low_score_blocks_story():
    result = review_story(FakeLLM([ai_says(calm=2, age_fit=3, quality=3)]), GOOD_550, "5-6", 5)
    assert result["approved"] is False          # total 8 < 12


def test_rules_veto_a_passing_ai_review():
    scary = GOOD_550 + " A monster."
    result = review_story(FakeLLM([ai_says()]), scary, "5-6", 5)
    assert result["review"].safety == "fail"    # AI said pass, the rules overruled it
    assert result["approved"] is False


def test_short_story_gets_length_fix_note():
    result = review_story(FakeLLM([ai_says()]), "The owl slept.", "5-6", 5)
    assert result["approved"] is False
    assert "length" in result["fix_notes"]