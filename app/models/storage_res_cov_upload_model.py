import datetime
import io
import re
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, computed_field, ConfigDict, field_validator

PREFIX_NAME = "kasun_nirmala"
BASE_FOLDER = "applied_jobs"


class StorageResCovUploadModel(BaseModel):
    type: Literal["resume", "cover"]
    company_name: str
    title_short: str

    @field_validator("company_name", mode="before")
    @classmethod
    def normalize_company_name(cls, value: str) -> str:
        return re.sub(r"[^a-zA-Z0-9]", "", value)

    @computed_field
    @property
    def file_name(self) -> str:
        curr_timestamp = datetime.datetime.now().timestamp()
        return f"{PREFIX_NAME}_{self.type}_{self.company_name}_{self.title_short}_{curr_timestamp}.pdf".lower()

    @computed_field
    @property
    def path(self) -> str:
        return f"{BASE_FOLDER}/{self.company_name}/{self.file_name}".lower()

    resume_data: io.BytesIO
    # @computed_field
    # @property
    # def resume_data(self) -> io.BytesIO:
    #     base_dir = Path(__file__).resolve().parent.parent.parent
    #     resume_key = base_dir / "assets" / "Kasun_Nirmala.pdf"
    #     file_path = Path(resume_key)
    #
    #     file_bytes = file_path.read_bytes()
    #
    #     file_obj = io.BytesIO(file_bytes)
    #     file_obj.seek(0)
    #
    #     return file_obj

    model_config = ConfigDict(arbitrary_types_allowed=True)
