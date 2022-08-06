from typing import Dict

from elasticsearch import Elasticsearch


class AppContext:
    def __init__(self, es: Elasticsearch, index: str) -> None:
        self.es = es
        self.index = index
        self._check_connection()


    def search_in_index(self, body: Dict) -> Dict:
        res = self.es.search(index=self.index, body=body)
        # log res?
        return res

    def _check_connection(self):
        if not self.es.ping():
            raise ValueError(f"Connection failed to {self.es}")


def create_es_client() -> Elasticsearch:
    # configure params
    return Elasticsearch(
        hosts=["https://localhost:9200"],
        http_auth=("admin", "admin"),
        verify_certs=False,
    )


def create_app_context(index_name="opensearch_dashboards_sample_data_ecommerce"):
    return AppContext(es=create_es_client(), index=index_name)
