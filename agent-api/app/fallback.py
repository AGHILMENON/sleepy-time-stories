"""Pre-approved stories, played if a generated story fails review 3 times.
A child must never hear an unchecked story (PRD safety rule S5)."""

FALLBACK_STORY = {
    "title": "Tiny Turtle and the Quiet Sea",
    "music_mood": "waves",
    "text": (
        "Tiny Turtle lived by the sea, in a warm spot of soft sand. "
        "Every evening the waves went shhh, shhh, and the sky turned pink, then orange, then gentle blue. "
        "Tiny Turtle watched the moon come up, round and kind. "
        "The breeze went whooo. Tiny Turtle breathed in slowly, and out slowly. "
        "Goodnight, moon. Goodnight, sea. And Tiny Turtle fell fast asleep. "
        "Goodnight, {CHILD}. Sleep tight."
    ),
}