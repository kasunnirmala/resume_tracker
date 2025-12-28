from datetime import timedelta
from io import BytesIO

from app.models.storage_res_cov_upload_model import StorageResCovUploadModel
from app.util.firebase import get_storage_bucket


class StorageUtils:

    def __init__(self):
        self.bucket = get_storage_bucket()

    def upload_res_cov(self, res_cov: StorageResCovUploadModel) -> str:
        blob = self.bucket.blob(res_cov.path)
        blob.upload_from_file(res_cov.resume_data, content_type="application/pdf")
        return res_cov.path

    def retrieve_file(self, path: str) -> BytesIO:
        blob = self.bucket.blob(path)
        return blob.download_as_bytes()

    def generate_public_url(self, path: str) -> str:
        blob = self.bucket.blob(path)
        return blob.generate_signed_url(
            expiration=timedelta(hours=1),
            method="GET"
        )
