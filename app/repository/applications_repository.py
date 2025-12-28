from google.cloud.firestore_v1.field_path import FieldPath

from app.models.application_model import ApplicationModel
from app.repository.base_repository import BaseRepository


class ApplicationsRepository(BaseRepository):

    def __init__(self):
        super().__init__()
        self.collection = self.db.collection("applications")

    def get_all_applications(self):
        return self.collection.stream()

    def get_by_ids(self, ids: list[str]):
        return self.collection.where(FieldPath.document_id(), 'in', ids).stream() if ids else []

    def create_application(self, application: ApplicationModel) -> str:
        doc_ref = self.collection.document()
        payload = {
            **application.model_dump(exclude_none=True),
        }
        doc_ref.set(payload)
        return doc_ref.id
