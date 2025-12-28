from typing import Annotated, Optional, Any

from fastapi import UploadFile
from pydantic import BaseModel, ConfigDict, BeforeValidator, field_validator


class AddApplicationFormData(BaseModel):
    company_name: str
    company_location: str
    job_title: str
    job_description: str
    resume: UploadFile
    cover_letter: Optional[UploadFile] = None
    other_details: str

    @field_validator("cover_letter", mode="plain")
    @classmethod
    def _check_content(cls, file: Optional[UploadFile]) -> Optional[UploadFile]:
        if isinstance(file, UploadFile):
            if file.size > 0:
                return file
        return None

    model_config = ConfigDict(extra="forbid")
