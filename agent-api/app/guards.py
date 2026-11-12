import re

from app.prompts import WORDS_PER_MINUTE

# Words that must never appear in a bedtime story (whole words, any case).
BANNED_WORDS = {
    "kill", "killed", "dead", "die", "died", "death", "blood", "monster", "monsters",
    "ghost", "witch", "demon", "gun", "knife", "sword", "fight", "fighting", "attack",
    "scream", "screamed", "terrified", "nightmare", "lost", "hurt", "sick", "hospital",
    "cry", "crying", "dragon",
}

LENGTH_TOLERANCE = 0.15   # a story may be 15% shorter or longer than the target


def find_banned(text: str) -> list[str]:
    """Return any banned words found in the text, sorted."""
    words = set(re.findall(r"[a-z']+", text.lower()))
    return sorted(words & BANNED_WORDS)


def rule_check(text: str, minutes: int) -> list[str]:
    """Return a list of problems. An empty list means the story passed."""
    problems = []

    banned = find_banned(text)
    if banned:
        problems.append(f"banned words: {', '.join(banned)}")

    count = len(text.split())
    target = minutes * WORDS_PER_MINUTE
    if abs(count - target) > LENGTH_TOLERANCE * target:
        problems.append(f"length is {count} words, target is about {target}")

    if text.count("{CHILD}") > 2:
        problems.append("the {CHILD} placeholder is used more than twice")

    if re.search(r"https?://|www\.", text):
        problems.append("the story contains a link")

    return problems