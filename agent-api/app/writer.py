from app.models import StoryRequest
from app.prompts import WORDS_PER_MINUTE, WRITER

MOODS = {"forest", "rain", "waves", "night"}


def write_story(llm, req: StoryRequest, fix_notes: str = "") -> dict:
    """Ask the AI for one story and return a clean result."""
    words = req.minutes * WORDS_PER_MINUTE

    system = WRITER.format(
        age=req.age_band,
        hero=req.hero,
        place=req.place.replace("_", " "),
        minutes=req.minutes,
        words=words,
    )

    request = "Write tonight's story."
    if fix_notes:
        request += f" The last draft was rejected. Fix this: {fix_notes}"
    draft = llm.complete_json(system, request)

    story = draft.get("story", "").strip()
    if not story:
        raise ValueError("The AI returned no story text.")

    mood = draft.get("music_mood", "night")
    if mood not in MOODS:
        mood = "night"

    return {
        "title": draft.get("title", "A Sleepy Story").strip(),
        "text": story,
        "music_mood": mood,
        "minutes": req.minutes,
        "target_words": words,
        "word_count": len(story.split()),
    }