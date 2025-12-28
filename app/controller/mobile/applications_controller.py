from fastapi import APIRouter

from app.controller.web.applications_controller import get_all_applications
from app.service.search_service import SearchService

router = APIRouter(prefix="/applications")
search_service = SearchService()


@router.get("/")
def get_all_applications():
    return get_all_applications()
