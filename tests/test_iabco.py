from app.algorithms.iabco import recommend_courses
from app.data.demo_courses import DEMO_COURSES
from app.models.student import StudentPreferences


def test_recommendations_are_deterministic_and_preference_aware():
    prefs = StudentPreferences(interests=["data"], skills=["python"], preferred_difficulty="beginner")
    first = recommend_courses(DEMO_COURSES, prefs)
    second = recommend_courses(DEMO_COURSES, prefs)
    assert [course.id for course in first] == [course.id for course in second]
    assert first[0].id == "demo-python"
    assert all(0 <= course.match_score <= 1 for course in first)


def test_empty_catalogue_returns_no_recommendations():
    assert recommend_courses([], StudentPreferences()) == []
