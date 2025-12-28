from typing import Annotated

from fastapi import APIRouter, Form
from pydantic import BaseModel

from app.models.add_application_form_data import AddApplicationFormData
from app.service.applications_service import ApplicationsService

router = APIRouter(prefix="/applications")
applications_service = ApplicationsService()


##TODO: ONLY FOR TESTING
class ApplicationSearchIds(BaseModel):
    ids: list[str]


@router.get("/")
def get_all_applications():
    return applications_service.get_all_applications()


@router.post("/ids")
def get_applications_by_ids(ids: ApplicationSearchIds):
    return applications_service.get_applications_by_ids(ids.ids)


@router.post("/")
async def add_application(application: Annotated[AddApplicationFormData, Form()]):
    return await applications_service.create_application(application)
