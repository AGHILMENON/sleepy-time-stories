from fastapi import Depends, FastAPI, HTTPException

from app.agent import generate_story
from app.llm import OllamaLLM
from app.models import StoryRequest

app = FastAPI(title="Sleepy Time Stories - Agent API")


def get_writer():
    return OllamaLLM("qwen3:8b")


def get_reviewer():
    return OllamaLLM("qwen3:14b")


@app.get("/healthz")
def healthz():
    return {"ok": True}


@app.post("/stories")
def create_story(req: StoryRequest, writer=Depends(get_writer), reviewer=Depends(get_reviewer)):
    try:
        return generate_story(writer, reviewer, req)
    except ValueError as e:
        raise HTTPException(status_code=502, detail=str(e))