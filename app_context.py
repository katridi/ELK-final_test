from elasticsearch import Elasticsearch


class AppContext:
    def __init__(self, es: Elasticsearch) -> None:
        self.es = es
        self._check_connection()
 
    def _check_connection(self) -> None:
        if not self.es.ping():
            raise ValueError(f"Connection failed to {self.es}")


def create_es_client() -> Elasticsearch:
    # configure params
    return Elasticsearch(
        hosts=["https://localhost:9200"],
        http_auth=("admin", "admin"),
        verify_certs=False,
        use_ssl=True,
        ssl_show_warn=False
    )


def create_app_context():
    return AppContext(es=create_es_client())