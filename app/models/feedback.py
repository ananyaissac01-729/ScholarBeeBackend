"""Feedback input and output schemas."""

from typing import Literal
from pydantic import BaseModel, Field


class FeedbackRequest(BaseModel):
    student_id: str = Field(min_length=1, max_length=100)
    course_id: str = Field(min_length=1, max_length=100)
    outcome: Literal["completed", "started", "skipped", "disliked"]


class FeedbackResponse(BaseModel):
    accepted: bool
    reward: float
    message: str
