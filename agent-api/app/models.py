from typing import Literal
from pydantic import BaseModel


class StoryRequest(BaseModel):
    model_config = {"extra": "forbid"}   # safety: rejects unknown fields like child_name
    age_band: Literal["3-4", "5-6", "7-8"]
    hero: Literal["elephant", "owl", "turtle", "bunny"]
    place: Literal["forest", "seaside", "starry_sky"]
    minutes: Literal[5, 10, 15]