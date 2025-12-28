from fastapi import APIRouter
from app.service.search_service import SearchService

router = APIRouter(prefix="/search")
search_service = SearchService()


@router.get("/")
def search_applications_mobile(text: str):
    return search_service.search_applications(text)
