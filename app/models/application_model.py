import datetime
from datetime import date

from pydantic import BaseModel

from app.models.job_model import JobModel


class ApplicationModel(BaseModel):
    id: str | None = None
    job_id: str | None = None
    job: JobModel | None = None
    resume_src: str
    cover_letter_src: str
    other_details: str
    applied_at: datetime.datetime = datetime.datetime.now()
    updated_at: datetime.datetime = datetime.datetime.now()
    created_at: datetime.datetime = datetime.datetime.now()
