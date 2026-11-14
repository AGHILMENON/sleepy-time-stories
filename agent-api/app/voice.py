import numpy as np

SAMPLE_RATE = 24000          # Kokoro produces 24,000 samples per second
CHILD_WORD = "little one"    # spoken instead of {CHILD}; the agent never knows the name


def prepare_for_voice(text: str) -> str:
    """Make story text safe and natural to read aloud."""
    return text.replace("{CHILD}", CHILD_WORD)


class FakeVoice:
    """Pretend voice for tests: returns silence, 0.1 seconds per word."""

    def __init__(self):
        self.calls = []

    def speak(self, text: str) -> np.ndarray:
        self.calls.append(text)
        seconds = 0.1 * len(text.split())
        return np.zeros(int(SAMPLE_RATE * seconds), dtype=np.float32)


class KokoroVoice:
    """Real local voice. Free, runs on your laptop."""

    def __init__(self, voice: str = "af_bella", speed: float = 0.85):
        from kokoro import KPipeline
        self.pipeline = KPipeline(lang_code="a")
        self.voice = voice
        self.speed = speed

    def speak(self, text: str) -> np.ndarray:
        parts = [audio for _, _, audio in self.pipeline(text, voice=self.voice, speed=self.speed)]
        return np.concatenate(parts).astype(np.float32)