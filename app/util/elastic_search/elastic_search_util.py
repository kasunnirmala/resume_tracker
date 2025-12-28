from typing import Iterable, Dict, Optional, List, Any, Mapping

from elastic_transport import ObjectApiResponse
from elasticsearch import Elasticsearch, NotFoundError
from elasticsearch.helpers import bulk

from app.modules.AI.helpers.vectorizer import text_embeddings


class ElasticSearchUtil:
    def __init__(
            self,
            index_name: str,
            host: str = "http://localhost:9200",
            auth: Optional[tuple] = None,
    ):
        self.index_name = index_name
        self.client = Elasticsearch(
            hosts=[host],
            basic_auth=auth,
            request_timeout=10,
            retry_on_timeout=True,
            max_retries=3,

        )

    def ensure_index(self, mappings: Dict, settings: Optional[Dict] = None):
        if self.client.indices.exists(index=self.index_name):
            return

        body = {"mappings": mappings}
        if settings:
            body["settings"] = settings

        self.client.indices.create(index=self.index_name, body=body)

    def delete_index(self):
        if self.client.indices.exists(index=self.index_name):
            self.client.indices.delete(index=self.index_name)

    def upsert(self, doc_id: str, document: Dict):
        self.client.index(
            index=self.index_name,
            id=doc_id,
            document=document,
        )

    def delete(self, doc_id: str):
        try:
            self.client.delete(index=self.index_name, id=doc_id)
        except NotFoundError:
            pass

    def bulk_upsert(self, documents: Iterable[Dict]):
        actions = []

        for doc in documents:
            actions.append({
                "_op_type": "index",
                "_index": self.index_name,
                "_id": doc["id"],
                "_source": doc,
            })

        if not actions:
            return

        bulk(self.client, actions)

    def rebuild(self, documents: Iterable[Dict], mappings: Dict):
        self.delete_index()
        self.ensure_index(mappings)
        self.bulk_upsert(documents)

    def search(
            self,
            query: Dict,
            from_: int = 0,
            size: int = 10,
            sort: Optional[Mapping[str, Any]] = None,
            source: Optional[List[str]] = None,
    ) -> ObjectApiResponse[Any]:
        body = {
            "query": query,
            "from": from_,
            "size": size,
        }

        if sort:
            body["sort"] = sort

        if source:
            body["_source"] = source

        return self.client.search(
            index=self.index_name,
            body=body,
        )

    def search_text(
            self,
            text: str,
            fields: List[str],
            from_: int = 0,
            size: int = 10,
    ) -> List[Dict]:
        query = {
            "multi_match": {
                "query": text,
                "fields": fields,
                "type": "cross_fields",
            }
        }
        res = self.search(query=query, from_=from_, size=size)
        return [hit["_source"] for hit in res["hits"]["hits"]]

    def search_with_filters(
            self,
            must: Optional[List[Dict]] = None,
            filters: Optional[List[Dict]] = None,
            from_: int = 0,
            size: int = 10,
    ) -> List[Dict]:
        query = {
            "bool": {
                "must": must or [],
                "filter": filters or [],
            }
        }

        res = self.search(query=query, from_=from_, size=size)
        return [hit["_source"] for hit in res["hits"]["hits"]]

    def count(self, query: Dict) -> int:
        res = self.client.count(
            index=self.index_name,
            query=query,
        )
        return res["count"]

    def search_vectors_knn(self, query: str, embed_field: str, k: int = 5):
        query_vector = text_embeddings(query)
        res = self.client.search(
            index=self.index_name,
            knn={
                "field": embed_field,
                "query_vector": query_vector,
                "k": k,
                "num_candidates": 100
            },
            _source=["content"]
        )

        return [
            {
                "score": hit["_score"],
                "content": hit["_source"]["content"],
            }
            for hit in res["hits"]["hits"]
        ]

    # def test_connection(self):
    #     try:
    #         print("Ping:", self.client.ping())
    #         print("Info:", self.client.info())
    #         print("Index name:", self.index_name)
    #         return True
    #     except Exception as e:
    #         print("Connection failed:", e)
    #         return False
