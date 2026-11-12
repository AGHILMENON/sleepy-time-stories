from app.guards import rule_check
from app.models import SafetyReview
from app.prompts import REVIEWER

PASS_TOTAL = 12   # calm + age_fit + quality must be at least 12 out of 15


def review_story(llm, text: str, age_band: str, minutes: int) -> dict:
    """Score a story with the AI reviewer AND the rule checks. Both must pass."""
    raw = llm.complete_json(REVIEWER.format(age=age_band), f"Story to review:\n\n{text}")
    review = SafetyReview(**raw)          # validates the AI's answer

    problems = rule_check(text, minutes)  # the rule layer
    if any(p.startswith("banned words") for p in problems):
        review.safety = "fail"            # rules can VETO the AI reviewer

    approved = review.safety == "pass" and review.total >= PASS_TOTAL and not problems

    fix_notes = " ".join(filter(None, [review.fix_notes, "; ".join(problems)]))

    return {
        "approved": approved,
        "review": review,
        "problems": problems,
        "fix_notes": fix_notes,
    }