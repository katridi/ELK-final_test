from operator import index
from elasticsearch import Elasticsearch


class AppContext:
    def __init__(self, es: Elasticsearch, index: str) -> None:
        self.es = es
        self.index = index


def create_es_client() -> Elasticsearch:
    # configure params
    return Elasticsearch(
        hosts=["https://localhost:9200"],
        http_auth=("admin", "admin"),
        verify_certs=False,
    )


def create_app_context(index_name="opensearch_dashboards_sample_data_ecommerce"):
    return AppContext(es=create_es_client(), index=index_name)
