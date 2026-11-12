from app.guards import find_banned, rule_check

GOOD_550 = " ".join(["The little owl yawned softly by the sea."] * 61)   # about 550 words


def test_good_story_passes():
    assert rule_check(GOOD_550, 5) == []


def test_finds_banned_words_any_case():
    assert find_banned("A Monster appeared. The ghost cried.") == ["ghost", "monster"]


def test_short_story_fails_length():
    problems = rule_check("The owl slept.", 5)
    assert any("length" in p for p in problems)


def test_too_many_child_placeholders():
    text = GOOD_550 + " {CHILD} {CHILD} {CHILD}"
    assert any("placeholder" in p for p in rule_check(text, 5))


def test_link_is_flagged():
    assert any("link" in p for p in rule_check(GOOD_550 + " www.example.com", 5))