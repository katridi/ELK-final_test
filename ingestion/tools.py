
import re
from typing import Dict

import urllib3
from elasticsearch import Elasticsearch
from elasticsearch.helpers import parallel_bulk
from elasticsearch_dsl import Index
from pandas import DataFrame

urllib3.disable_warnings()


def set_index_settings(es: Elasticsearch, index_name: str, settings: Dict) -> None:
    i = Index(name=index_name, using=es)
    i.settings(**settings)


def extract_year(string):
    pattern = r"[(]\d{4}[)]"
    matches = re.findall(pattern, string)
    if matches:
        return matches[0].replace("(", "").replace(")", "")
    return


def replace_year(string):
    pattern = r"[(]\d{4}[)]"
    return re.sub(pattern, "", string, 1).strip()


def data_iterator(index_string_name: str, table: DataFrame):
    my_iterator = iter(table.to_dict("records"))
    counter = 0
    while my_iterator:
        try:
            value = next(my_iterator)
            yield {"_index": index_string_name, "_id": counter, **value}
            counter += 1
        except StopIteration:
            break


def create_elastic_client() -> Elasticsearch:
    return Elasticsearch(hosts=["https://localhost:9200"], http_auth=("admin", "admin"), verify_certs=False)


def ingest_data(es: Elasticsearch, data: DataFrame, index_name: str, thread_count: int = 8, chunk_size: int = 1000) -> None:
    es.ping()
    for success, info in parallel_bulk(es, data_iterator(index_name, data), thread_count=thread_count, chunk_size=chunk_size):
        if not success:
            print("A document failed:", info)
