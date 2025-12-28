from fastapi import APIRouter
from app.controller.mobile.search_controller_mobile import router as search_controller_mobile
from app.controller.mobile.applications_controller_mobile import router as applications_controller_mobile

mobile_router = APIRouter(
    prefix="/api/mobile",
    tags=["Mobile"]
)

mobile_router.include_router(search_controller_mobile)
mobile_router.include_router(applications_controller_mobile)
