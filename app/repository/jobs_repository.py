from app.models.job_model import JobModel
from app.repository.base_repository import BaseRepository


class JobsRepository(BaseRepository):

    def __init__(self):
        super().__init__()
        self.collection = self.db.collection("jobs")

    def get_all_jobs(self):
        return self.collection.stream()

    def get_job_by_id(self, job_id : str):
        return self.collection.document(job_id).get()

    def create_job(self, job: JobModel) -> str:
        doc_ref = self.collection.document()
        payload = {
            **job.model_dump(exclude_none=True),
        }
        doc_ref.set(payload)
        return doc_ref.id
