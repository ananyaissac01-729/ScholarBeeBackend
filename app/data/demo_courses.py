"""Illustrative course catalogue only; replace with verified production data."""

from app.models.course import Course

DEMO_COURSES: list[Course] = [
    Course(id="demo-python", title="Python Foundations (Demo)", description="Introductory programming concepts and Python basics.", interests=["programming", "data"], skills=["python", "coding"], difficulty="beginner"),
    Course(id="demo-data", title="Data Analysis Basics (Demo)", description="Explore datasets with practical analysis exercises.", interests=["data", "analytics"], skills=["python", "statistics"], difficulty="intermediate"),
    Course(id="demo-ml", title="Machine Learning Primer (Demo)", description="A first look at supervised learning concepts.", interests=["ai", "data", "machine learning"], skills=["python", "math"], difficulty="advanced"),
    Course(id="demo-design", title="UX Design Essentials (Demo)", description="Learn user research and interface design fundamentals.", interests=["design", "technology"], skills=["research", "prototyping"], difficulty="beginner"),
    Course(id="demo-cloud", title="Cloud Computing Overview (Demo)", description="Understand cloud services and deployment concepts.", interests=["cloud", "technology"], skills=["networking", "linux"], difficulty="intermediate"),
]
