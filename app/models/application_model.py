from datetime import date

from pydantic import BaseModel

class ApplicationModel(BaseModel):
    id: str
    job_id: str
    resume_src: str
    cover_letter_src: str
    other_details: str
    applied_at: date
    updated_at: date
    created_at: date
