import json

from app.config.config import get_settings
from app.models.application_model import ApplicationModel
from app.modules.AI.helpers.vectorizer import text_embeddings
from app.service.applications_service import ApplicationsService
from app.util.elastic_search.elastic_search_util import ElasticSearchUtil
from app.util.elastic_search.es_mappings import APPLICATION_MAPPINGS, APPLICATION_VECTOR_MAPPINGS


class SearchService:
    def __init__(self):
        self.application_elastic_search = ElasticSearchUtil(
            index_name=get_settings().application_es_collection
        )
        self.application_vector = ElasticSearchUtil(
            index_name=get_settings().application_vector_es_collection
        )
        self.application_service = ApplicationsService()

    def search_applications(self, text: str) -> list[ApplicationModel]:
        search_result = self.application_elastic_search.search_text(
            text=text,
            fields=list(APPLICATION_MAPPINGS["properties"].keys())
        )
        return self.application_service.get_applications_by_ids(
            ids=[result["id"] for result in search_result]
        )
        # search_result = self.application_vector.search_vectors_knn(query=text, embed_field="embedding")
        # return self.application_service.get_applications_by_ids(
        #     ids=[json.loads(result["content"])["id"] for result in search_result]
        # )

    def rebuild_es(self) -> bool:
        flatten_applications: list[dict] = self.application_service.get_all_applications(flatten=True)

        self.application_elastic_search.rebuild(
            documents=flatten_applications,
            mappings=APPLICATION_MAPPINGS
        )
        vectored_applications = []
        for application in flatten_applications:
            vectored_applications.append({
                "id": application["id"],
                "content": json.dumps(application, default=str),
                "embedding": text_embeddings(json.dumps(application, default=str))
            })
        self.application_vector.rebuild(
            documents=vectored_applications,
            mappings=APPLICATION_VECTOR_MAPPINGS
        )
        return True
