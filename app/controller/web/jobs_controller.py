from fastapi import APIRouter

from app.models.job_model import JobModel
from app.service.jobs_service import JobsService

router = APIRouter(prefix="/jobs")
jobs_service = JobsService()


@router.get("/")
def get_all_jobs():
    return jobs_service.get_all_jobs()


@router.post("/")
def create_job(job: JobModel):
    return jobs_service.create_job(job)
