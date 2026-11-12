from app.fallback import FALLBACK_STORY
from app.models import StoryRequest
from app.reviewer import review_story
from app.writer import write_story

MAX_ATTEMPTS = 3   # first draft + 2 rewrites


def generate_story(writer_llm, reviewer_llm, req: StoryRequest) -> dict:
    """Write, review, rewrite until approved, or fall back to a safe story."""
    fix_notes = ""
    trace = []                                   # a log of every step, for debugging

    for attempt in range(1, MAX_ATTEMPTS + 1):
        story = write_story(writer_llm, req, fix_notes)
        result = review_story(reviewer_llm, story["text"], req.age_band, req.minutes)

        trace.append({
            "attempt": attempt,
            "word_count": story["word_count"],
            "safety": result["review"].safety,
            "score": result["review"].total,
            "problems": result["problems"],
            "approved": result["approved"],
        })

        if result["approved"]:
            return {**story, "status": "approved", "attempts": attempt, "trace": trace}

        fix_notes = result["fix_notes"]          # feed the notes into the next draft

    return {
        **FALLBACK_STORY,
        "minutes": req.minutes,
        "status": "fallback_used",
        "attempts": MAX_ATTEMPTS,
        "trace": trace,
    }