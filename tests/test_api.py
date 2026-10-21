import pytest
from fastapi import HTTPException

from app.api.routes.courses import list_courses
from app.api.routes.feedback import submit_feedback
from app.api.routes.health import health_check
from app.api.routes.recommendations import RecommendationRequest, create_recommendations
from app.models.feedback import FeedbackRequest


def test_health_and_demo_catalogue():
    assert health_check()["status"] == "ok"
    courses = list_courses()
    assert courses
    assert all(course.demo_data for course in courses)


def test_recommendation_and_feedback_route_logic():
    request = RecommendationRequest.model_validate({
        "student_id": "student-1",
        "preferences": {"interests": ["data"], "skills": ["python"], "preferred_difficulty": "beginner"},
        "limit": 3,
    })
    response = create_recommendations(request)
    assert len(response.recommendations) == 3
    assert "not validated" in response.algorithm_status

    feedback = submit_feedback(FeedbackRequest(student_id="student-1", course_id="demo-python", outcome="completed"))
    assert feedback.reward == 1.0


def test_invalid_preference_and_unknown_course_errors():
    with pytest.raises(ValueError):
        RecommendationRequest.model_validate({"student_id": "s", "preferences": {"preferred_difficulty": "expert"}})
    with pytest.raises(HTTPException) as error:
        submit_feedback(FeedbackRequest(student_id="s", course_id="missing", outcome="completed"))
    assert error.value.status_code == 404
