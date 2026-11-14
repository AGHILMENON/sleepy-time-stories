from pathlib import Path

import soundfile as sf

from app.voice import SAMPLE_RATE, prepare_for_voice


def narrate(voice, story: dict, out_dir: str = "audio") -> dict:
    """Read an approved story aloud and save it as a WAV file."""
    text = prepare_for_voice(story["text"])
    audio = voice.speak(text)

    Path(out_dir).mkdir(exist_ok=True)
    safe_title = "".join(c if c.isalnum() else "_" for c in story["title"])[:40]
    path = Path(out_dir) / f"{safe_title}.wav"
    sf.write(path, audio, SAMPLE_RATE)

    return {"audio_path": str(path), "duration_seconds": round(len(audio) / SAMPLE_RATE)}