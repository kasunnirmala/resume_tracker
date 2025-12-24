from app.models.job_model import JobModel
from app.repository.jobs_repository import JobsRepository


class JobsService:
    def __init__(self):
        self.jobs_repository = JobsRepository()

    def get_all_jobs(self) -> list[JobModel]:
        all_jobs = self.jobs_repository.get_all_jobs()
        return [JobModel(id=job.id, **job.to_dict()) for job in all_jobs]

    def create_job(self, job: JobModel) -> JobModel:
        job.id = self.jobs_repository.create_job(job)
        return job
