from fastapi import APIRouter

mobile_router = APIRouter(
    prefix="/api/mobile",
    tags=["Mobile"]
)

# mobile_router.include_router(mobile_controller)
