from functools import lru_cache
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.agent import generate_story
from app.llm import OllamaLLM
from app.models import StoryRequest
from app.narrator import narrate

AUDIO_DIR = Path("audio")
AUDIO_DIR.mkdir(exist_ok=True)

app = FastAPI(title="Sleepy Time Stories - Agent API")

# Let the React web page (running on another port) call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Serve the finished audio files at /audio/<file>.wav
app.mount("/audio", StaticFiles(directory=AUDIO_DIR), name="audio")


def get_writer():
    return OllamaLLM("qwen3:8b")


def get_reviewer():
    return OllamaLLM("qwen3:14b")


@lru_cache
def get_voice():
    from app.voice import KokoroVoice
    return KokoroVoice()              # loaded once, then reused


@app.get("/healthz")
def healthz():
    return {"ok": True}


@app.post("/stories")
def create_story(
    req: StoryRequest,
    writer=Depends(get_writer),
    reviewer=Depends(get_reviewer),
    voice=Depends(get_voice),
):
    try:
        story = generate_story(writer, reviewer, req)
    except ValueError as e:
        raise HTTPException(status_code=502, detail=str(e))

    audio = narrate(voice, story, out_dir=str(AUDIO_DIR))
    file_name = Path(audio["audio_path"]).name
    return {
        **story,
        "audio_url": f"/audio/{file_name}",
        "duration_seconds": audio["duration_seconds"],
        "music": audio["music"],
    }