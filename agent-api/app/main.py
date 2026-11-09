from fastapi import FastAPI
from typing import Literal
from pydantic import BaseModel

app = FastAPI(title="Sleepy Time Stories - Agent API")
class StoryRequest(BaseModel):
    model_config = {"extra": "forbid"}
    age_band: Literal["3-4", "5-6", "7-8"]
    hero: Literal["elephant", "owl", "turtle", "bunny"]
    place: Literal["forest", "seaside", "starry_sky"]
    minutes: Literal[5, 10, 15]

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.post("/stories")
def create_story(req: StoryRequest):
    return {
        "title": f"The {req.hero.title()} in the {req.place.replace('_', ' ')}",
        "text": f"Once upon a time, a sleepy {req.hero}... Goodnight, {{CHILD}}.",
        "minutes": req.minutes,
    }