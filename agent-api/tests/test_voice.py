from app.narrator import narrate
from app.voice import FakeVoice, prepare_for_voice


def test_child_placeholder_is_never_spoken():
    assert prepare_for_voice("Goodnight, {CHILD}.") == "Goodnight, little one."


def test_narrate_saves_wav_and_reports_duration(tmp_path):
    voice = FakeVoice()
    story = {"title": "Owl's Quiet Night", "text": "The owl yawned. Goodnight, {CHILD}."}
    result = narrate(voice, story, out_dir=str(tmp_path), music_dir=tmp_path)

    assert result["audio_path"].endswith("Owl_s_Quiet_Night.wav")
    assert (tmp_path / "Owl_s_Quiet_Night.wav").exists()
    assert result["duration_seconds"] == 1           # 6 words x 0.1 s, rounded
    assert "{CHILD}" not in voice.calls[0]           # the voice never saw the placeholder

import numpy as np

from app.mixer import MUSIC_UNDER, OUTRO_SECONDS, loop_to_length, mix
from app.voice import SAMPLE_RATE


def test_loop_makes_music_long_enough():
    music = np.ones(10, dtype=np.float32)
    assert len(loop_to_length(music, 25)) == 25


def test_mix_length_and_silent_ending():
    voice = np.zeros(SAMPLE_RATE * 3, dtype=np.float32)   # 3 s of (silent) voice
    music = np.ones(SAMPLE_RATE, dtype=np.float32) * 0.5  # 1 s of steady "music"
    track = mix(voice, music)
    assert len(track) == SAMPLE_RATE * (5 + 3 + OUTRO_SECONDS)
    assert abs(track[-1]) < 0.001                          # ends in silence


def test_music_is_ducked_under_voice():
    voice = np.zeros(SAMPLE_RATE * 10, dtype=np.float32)
    music = np.ones(SAMPLE_RATE, dtype=np.float32)
    track = mix(voice, music)
    middle_of_story = 5 * SAMPLE_RATE + 5 * SAMPLE_RATE
    assert abs(track[middle_of_story] - MUSIC_UNDER) < 0.01

def test_narrate_mixes_music_when_available(tmp_path):
    import soundfile as sf
    sf.write(tmp_path / "night.wav", np.zeros(SAMPLE_RATE, dtype=np.float32), SAMPLE_RATE)
    (tmp_path / "night.mp3").write_bytes((tmp_path / "night.wav").read_bytes())

    story = {"title": "Owl", "text": "The owl yawned.", "music_mood": "night"}
    result = narrate(FakeVoice(), story, out_dir=str(tmp_path), music_dir=tmp_path)

    assert result["music"] == "night.mp3"
    assert result["duration_seconds"] == 5 + OUTRO_SECONDS     # 5 s intro + 0.3 s voice + 60 s outro, rounded
