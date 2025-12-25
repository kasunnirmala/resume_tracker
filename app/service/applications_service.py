from app.models.application_model import ApplicationModel
from app.models.job_model import JobModel
from app.repository.applications_repository import ApplicationsRepository
from app.repository.jobs_repository import JobsRepository


class ApplicationsService:
    def __init__(self):
        self.jobs_repository = JobsRepository()
        self.applications_repository = ApplicationsRepository()

    def get_all_applications(self) -> list[ApplicationModel]:
        all_applications = self.applications_repository.get_all_applications()
        applications: list[ApplicationModel] = []
        for application_doc in all_applications:
            application = ApplicationModel(id=application_doc.id, **application_doc.to_dict())
            job = self.jobs_repository.get_job_by_id(application.job_id)
            application.job = JobModel(id=job.id, **job.to_dict())
            applications.append(application)
        return applications

    def create_application(self, application: ApplicationModel) -> ApplicationModel:
        created_job_id = self.jobs_repository.create_job(application.job)
        application.job_id = created_job_id
        application.job = None
        application.id = self.applications_repository.create_application(application)
        return application
