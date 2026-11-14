from app.narrator import narrate
from app.voice import FakeVoice, prepare_for_voice


def test_child_placeholder_is_never_spoken():
    assert prepare_for_voice("Goodnight, {CHILD}.") == "Goodnight, little one."


def test_narrate_saves_wav_and_reports_duration(tmp_path):
    voice = FakeVoice()
    story = {"title": "Owl's Quiet Night", "text": "The owl yawned. Goodnight, {CHILD}."}
    result = narrate(voice, story, out_dir=str(tmp_path))

    assert result["audio_path"].endswith("Owl_s_Quiet_Night.wav")
    assert (tmp_path / "Owl_s_Quiet_Night.wav").exists()
    assert result["duration_seconds"] == 1           # 6 words x 0.1 s, rounded
    assert "{CHILD}" not in voice.calls[0]           # the voice never saw the placeholder