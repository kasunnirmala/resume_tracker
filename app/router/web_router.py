from fastapi import APIRouter
from app.controller.web.jobs_controller import router as jobs_controller

web_router = APIRouter(
    prefix="/api/web",
    tags=["Web"]
)

web_router.include_router(jobs_controller)
