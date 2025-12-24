from pydantic import BaseModel


class JobModel(BaseModel):
    id: str | None = None
    company_name: str
    company_location: str
    job_title: str
    job_posted_date: str | None = None
    job_description: str
