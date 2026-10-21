from fastapi import APIRouter, HTTPException
from app.data.demo_courses import DEMO_COURSES
from app.models.feedback import FeedbackRequest, FeedbackResponse
from app.services.feedback import REWARDS, feedback_store

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.post("", response_model=FeedbackResponse, status_code=201)
def submit_feedback(request: FeedbackRequest) -> FeedbackResponse:
    """Record feedback using documented fixed reward rules (demo memory only)."""
    if request.course_id not in {course.id for course in DEMO_COURSES}:
        raise HTTPException(status_code=404, detail="Course not found")
    reward = feedback_store.record(request.student_id, request.course_id, request.outcome)
    return FeedbackResponse(accepted=True, reward=reward,
                            message=f"Feedback recorded. Reward rule: {request.outcome} = {REWARDS[request.outcome]:+g}.")
