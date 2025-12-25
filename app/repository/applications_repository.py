from app.models.application_model import ApplicationModel
from app.models.job_model import JobModel
from app.repository.base_repository import BaseRepository


class ApplicationsRepository(BaseRepository):

    def __init__(self):
        super().__init__()
        self.collection = self.db.collection("applications")

    def get_all_applications(self):
        return self.collection.stream()

    def create_application(self, application: ApplicationModel) -> str:
        doc_ref = self.collection.document()
        payload = {
            **application.model_dump(exclude_none=True),
        }
        doc_ref.set(payload)
        return doc_ref.id
