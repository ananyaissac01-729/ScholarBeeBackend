"""Student preference schemas used by recommendation requests."""

from typing import Literal
from pydantic import BaseModel, Field


class StudentPreferences(BaseModel):
    interests: list[str] = Field(default_factory=list, max_length=20, description="Topics the student is interested in")
    skills: list[str] = Field(default_factory=list, max_length=20, description="Topics or skills the student already knows")
    preferred_difficulty: Literal["beginner", "intermediate", "advanced"] = "beginner"
