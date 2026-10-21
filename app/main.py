"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import courses, feedback, health, recommendations
from app.core.config import settings

app = FastAPI(title=settings.app_name, version="0.1.0", description="Student course recommendations with clearly labelled demo data.")
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins,
                   allow_credentials=False, allow_methods=["GET", "POST"], allow_headers=["*"])
app.include_router(health.router)
app.include_router(courses.router)
app.include_router(recommendations.router)
app.include_router(feedback.router)
