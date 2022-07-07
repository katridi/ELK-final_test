from typing import Dict


def match_term(term, value: str) -> Dict:
    term = "customer_first_name.keyword"
    return {"query": {"term": {term: {"value": value}}}}
