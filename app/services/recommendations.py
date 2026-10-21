"""Recommendation service: connects preferences to the IABCO prototype."""

from app.algorithms.iabco import recommend_courses
from app.data.demo_courses import DEMO_COURSES
from app.models.course import RecommendedCourse
from app.models.student import StudentPreferences
from app.services.feedback import feedback_store


def get_recommendations(student_id: str, preferences: StudentPreferences, limit: int = 5) -> list[RecommendedCourse]:
    return recommend_courses(DEMO_COURSES, preferences, limit=limit,
                             adjustments=feedback_store.adjustments_for(student_id))
