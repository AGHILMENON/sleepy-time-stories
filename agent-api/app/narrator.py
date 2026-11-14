from pathlib import Path

import soundfile as sf

from app.mixer import load_music, mix
from app.voice import SAMPLE_RATE, prepare_for_voice

MUSIC_DIR = Path("music")


def narrate(voice, story: dict, out_dir: str = "audio", music_dir: Path = MUSIC_DIR) -> dict:
    """Read an approved story aloud over nature music and save the bedtime track."""
    text = prepare_for_voice(story["text"])
    speech = voice.speak(text)

    mood = story.get("music_mood", "night")
    music_file = Path(music_dir) / f"{mood}.mp3"
    track = mix(speech, load_music(str(music_file))) if music_file.exists() else speech

    Path(out_dir).mkdir(exist_ok=True)
    safe_title = "".join(c if c.isalnum() else "_" for c in story["title"])[:40]
    path = Path(out_dir) / f"{safe_title}.wav"
    sf.write(path, track, SAMPLE_RATE)

    return {
        "audio_path": str(path),
        "duration_seconds": round(len(track) / SAMPLE_RATE),
        "music": music_file.name if music_file.exists() else None,
    }