import numpy as np
import soundfile as sf

from app.voice import SAMPLE_RATE

INTRO_SECONDS = 5      # music alone before the story starts
OUTRO_SECONDS = 60     # music after the story, fading to silence
MUSIC_INTRO = 0.25     # music volume before the voice
MUSIC_UNDER = 0.08     # music volume while the voice speaks (ducking)
MUSIC_OUTRO = 0.20     # music volume when the story ends, before fading


def load_music(path: str) -> np.ndarray:
    """Load a music file as mono audio at our sample rate."""
    audio, rate = sf.read(path, dtype="float32")
    if audio.ndim == 2:                       # stereo -> mono
        audio = audio.mean(axis=1)
    if rate != SAMPLE_RATE:                   # resample to 24,000 per second
        old_times = np.arange(len(audio)) / rate
        new_times = np.arange(int(len(audio) * SAMPLE_RATE / rate)) / SAMPLE_RATE
        audio = np.interp(new_times, old_times, audio).astype(np.float32)
    return audio


def loop_to_length(music: np.ndarray, length: int) -> np.ndarray:
    """Repeat the music until it is exactly `length` samples long."""
    repeats = length // len(music) + 1
    return np.tile(music, repeats)[:length]


def mix(voice: np.ndarray, music: np.ndarray) -> np.ndarray:
    """Place the voice over looping music, duck the music, then fade to silence."""
    intro = INTRO_SECONDS * SAMPLE_RATE
    outro = OUTRO_SECONDS * SAMPLE_RATE
    total = intro + len(voice) + outro

    bed = loop_to_length(music, total)

    # Volume plan: points in time (samples) and the music volume at each point.
    voice_start, voice_end = intro, intro + len(voice)
    times = [0, voice_start - SAMPLE_RATE, voice_start, voice_end, voice_end + 2 * SAMPLE_RATE, total]
    volumes = [MUSIC_INTRO, MUSIC_INTRO, MUSIC_UNDER, MUSIC_UNDER, MUSIC_OUTRO, 0.0]
    envelope = np.interp(np.arange(total), times, volumes).astype(np.float32)

    track = bed * envelope
    track[voice_start:voice_end] += voice

    peak = np.abs(track).max()
    if peak > 0.98:                           # avoid crackling (clipping)
        track = track * (0.98 / peak)
    return track