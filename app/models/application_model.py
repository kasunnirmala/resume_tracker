import datetime
from pydantic import BaseModel

from app.models.job_model import JobModel


class ApplicationModel(BaseModel):
    id: str | None = None
    job_id: str | None = None
    job: JobModel | None = None
    resume_src: str | None = None
    cover_letter_src: str | None = None
    other_details: str | None = None
    summary: str | None = None
    applied_at: datetime.datetime = datetime.datetime.now()
    updated_at: datetime.datetime = datetime.datetime.now()
    created_at: datetime.datetime = datetime.datetime.now()
