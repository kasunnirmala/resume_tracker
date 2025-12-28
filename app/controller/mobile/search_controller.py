from fastapi import APIRouter
from app.service.search_service import SearchService

router = APIRouter(prefix="/search")
search_service = SearchService()


@router.get("/")
def search_applications(text: str):
    return search_service.search_applications(text)


@router.get("/reset")
def search_reset():
    return search_service.rebuild_es()
