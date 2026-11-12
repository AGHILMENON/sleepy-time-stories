from typing import Literal
from pydantic import BaseModel
from pydantic import Field



class StoryRequest(BaseModel):
    model_config = {"extra": "forbid"}   # safety: rejects unknown fields like child_name
    age_band: Literal["3-4", "5-6", "7-8"]
    hero: Literal["elephant", "owl", "turtle", "bunny"]
    place: Literal["forest", "seaside", "starry_sky"]
    minutes: Literal[5, 10, 15]


class SafetyReview(BaseModel):
    safety: Literal["pass", "fail"]
    safety_reasons: list[str] = []
    calm: int = Field(ge=1, le=5)
    age_fit: int = Field(ge=1, le=5)
    quality: int = Field(ge=1, le=5)
    fix_notes: str = ""

    @property
    def total(self) -> int:
        return self.calm + self.age_fit + self.quality