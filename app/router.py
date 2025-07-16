from fastapi import APIRouter
from app.surveys.routes import router as surveys_routes

api_router = APIRouter()
prefix = "/api/v1"

api_router.include_router(surveys_routes, prefix=prefix)