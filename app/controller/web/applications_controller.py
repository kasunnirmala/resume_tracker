from fastapi import APIRouter

from app.models.application_model import ApplicationModel
from app.models.job_model import JobModel
from app.service.applications_service import ApplicationsService
from app.service.jobs_service import JobsService

router = APIRouter(prefix="/applications")
applications_service = ApplicationsService()


@router.get("/")
def get_all_applications():
    return applications_service.get_all_applications()


@router.post("/")
def add_application(application: ApplicationModel):
    return applications_service.create_application(application)
