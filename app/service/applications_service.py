import io
import json
from typing import List, Tuple, Optional, Dict

from app.config.config import get_settings
from app.config.resume_data import get_resume_data
from app.models.add_application_form_data import AddApplicationFormData
from app.models.application_model import ApplicationModel
from app.models.job_model import JobModel
from app.models.storage_res_cov_upload_model import StorageResCovUploadModel
from app.modules.AI.application_summarizer import ApplicationSummarizer
from app.modules.AI.helpers.vectorizer import text_embeddings
from app.repository.applications_repository import ApplicationsRepository
from app.repository.jobs_repository import JobsRepository
from app.util.elastic_search.elastic_search_util import ElasticSearchUtil
from app.util.storage_utils import StorageUtils
import pandas as pd


class ApplicationsService:
    def __init__(self):
        self.jobs_repository = JobsRepository()
        self.applications_repository = ApplicationsRepository()
        self.storage_utils = StorageUtils()
        self.application_elastic_search = ElasticSearchUtil(
            index_name=get_settings().application_es_collection
        )
        self.application_vector = ElasticSearchUtil(
            index_name=get_settings().application_vector_es_collection
        )
        self.application_summarizer = ApplicationSummarizer()

    def get_all_applications(self, flatten=False) -> list[ApplicationModel] | list[dict] | None:
        all_applications = self.applications_repository.get_all_applications()
        applications, flatten_applications = self._dict_to_application_model(all_applications, flatten=flatten)
        return flatten_applications if flatten else applications

    def get_applications_by_ids(self, ids: list[str]) -> list[ApplicationModel]:
        all_applications = self.applications_repository.get_by_ids(ids)
        applications, _ = self._dict_to_application_model(all_applications)
        return applications

    async def create_application(self, data: AddApplicationFormData) -> ApplicationModel:
        application = ApplicationModel()
        job = JobModel(
            company_name=data.company_name,
            company_location=data.company_location,
            job_title=data.job_title,
            job_description=data.job_description
        )
        application.other_details = data.other_details

        resume_content = await data.resume.read()
        resume = StorageResCovUploadModel(
            type="resume",
            company_name=data.company_name,
            title_short="SSE",
            resume_data=io.BytesIO(resume_content)
        )
        resume_uploaded_path = self.storage_utils.upload_res_cov(resume)
        application.resume_src = resume_uploaded_path

        if data.cover_letter:
            cover_content = await data.cover_letter.read()
            cover = StorageResCovUploadModel(
                type="cover",
                company_name=data.company_name,
                title_short="SSE",
                resume_data=io.BytesIO(cover_content)
            )
            cover_uploaded_path = self.storage_utils.upload_res_cov(cover)
            application.cover_letter_src = cover_uploaded_path

        created_job_id = self.jobs_repository.create_job(job)
        application.job_id = created_job_id
        application.job = job
        application.summary = self.application_summarizer.summarize(
            content=application.model_dump_json(),
            resume_data=get_resume_data(),  ### TODO : REPLACE WITH PDFS PARSER
            cover_data=get_resume_data() if data.cover_letter else ""
        )
        application.job = None
        application.id = self.applications_repository.create_application(application)
        application.job = job
        self.application_elastic_search.upsert(application.id, application.model_dump())
        self.application_vector.upsert(application.id, {
            "id": application.id,
            "content": application.model_dump_json(),
            "embedding": text_embeddings(application.model_dump_json())
        })

        return application

    def _dict_to_application_model(self, all_applications: List, flatten=False) -> Tuple[
        List[ApplicationModel], Optional[List[Dict]]]:
        applications: list[ApplicationModel] = []
        flatten_applications = [] if flatten else None
        for application_doc in all_applications:
            application = ApplicationModel(id=application_doc.id, **application_doc.to_dict())
            job = self.jobs_repository.get_job_by_id(application.job_id)
            application.job = JobModel(id=job.id, **job.to_dict())
            applications.append(application)
            if flatten:
                flattened = pd.json_normalize(application.model_dump())
                flattened.astype(str)
                flatten_applications.extend(flattened.to_dict(orient="records"))
        return applications, flatten_applications
