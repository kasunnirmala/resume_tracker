from fastapi import APIRouter
from app.controller.mobile.search_controller import router as search_controller
from app.controller.mobile.applications_controller import router as applications_controller

mobile_router = APIRouter(
    prefix="/api/mobile",
    tags=["Mobile"]
)

mobile_router.include_router(search_controller)
mobile_router.include_router(applications_controller)
