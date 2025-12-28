from app.models.application_model import ApplicationModel
from app.service.applications_service import ApplicationsService
from app.util.elastic_search.elastic_search_util import ElasticSearchUtil
from app.util.elastic_search.es_mappings import APPLICATION_MAPPINGS


class SearchService:
    def __init__(self):
        self.application_elastic_search = ElasticSearchUtil(index_name="application")
        self.application_service = ApplicationsService()

    def search_applications(self, text: str) -> list[ApplicationModel]:
        search_result = self.application_elastic_search.search_text(
            text=text,
            fields=list(APPLICATION_MAPPINGS["properties"].keys())
        )
        return self.application_service.get_applications_by_ids(
            ids=[result["id"] for result in search_result]
        )
