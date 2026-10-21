"""Course catalogue and recommendation response schemas."""

from pydantic import BaseModel, Field


class Course(BaseModel):
    id: str
    title: str
    description: str
    interests: list[str]
    skills: list[str]
    difficulty: str
    demo_data: bool = True


class RecommendedCourse(Course):
    match_score: float = Field(ge=0, le=1)
    reason: str
