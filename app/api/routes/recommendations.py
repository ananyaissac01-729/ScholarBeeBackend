from fastapi import APIRouter, Query
from pydantic import BaseModel, Field
from app.models.course import RecommendedCourse
from app.models.student import StudentPreferences
from app.services.recommendations import get_recommendations

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


class RecommendationRequest(BaseModel):
    student_id: str = Field(min_length=1, max_length=100)
    preferences: StudentPreferences
    limit: int = Field(default=5, ge=1, le=20)


class RecommendationResponse(BaseModel):
    recommendations: list[RecommendedCourse]
    algorithm_status: str = "research-inspired prototype; not validated as a faithful paper reproduction"


@router.post("", response_model=RecommendationResponse)
def create_recommendations(request: RecommendationRequest) -> RecommendationResponse:
    recommendations = get_recommendations(request.student_id, request.preferences, request.limit)
    return RecommendationResponse(recommendations=recommendations)
