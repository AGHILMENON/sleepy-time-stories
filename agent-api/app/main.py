from fastapi import Depends, FastAPI, HTTPException

from app.llm import OllamaLLM
from app.models import StoryRequest
from app.writer import write_story

app = FastAPI(title="Sleepy Time Stories - Agent API")


def get_llm():
    """Which AI plug the app uses. Tests replace this with FakeLLM."""
    return OllamaLLM("qwen3:8b")


@app.get("/healthz")
def healthz():
    return {"ok": True}


@app.post("/stories")
def create_story(req: StoryRequest, llm=Depends(get_llm)):
    try:
        return write_story(llm, req)
    except ValueError as e:
        raise HTTPException(status_code=502, detail=str(e))