from fastapi import APIRouter
from app.data.demo_courses import DEMO_COURSES
from app.models.course import Course

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("", response_model=list[Course])
def list_courses() -> list[Course]:
    """Return the current demo catalogue. Replace it with verified course data."""
    return DEMO_COURSES
