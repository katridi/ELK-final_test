from typing import Dict


def match_term(term: str, value: str) -> Dict:
    return {"query": {"term": {term: {"value": value}}}}


def fuzzy_term(term: str, value: str) -> Dict:
    return {"query": {"fuzzy": {term: {"value": value}}}}
