from __future__ import annotations
from turtle import title

from typing import List, Optional

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Document, Float, Integer, Keyword, Text, Q


class Movies(Document):
    movieId = Integer()
    title = Text()
    genres = Keyword(multi=True)
    year = Integer()
    imdbId = Integer()
    tmdbId = Integer()
    tag = Keyword(multi=True)
    relevance = Float(multi=True)

    class Index:
        name = "movies"
        settings = {
            "refresh_interval": "1",
            "number_of_shards": "1",
        }

    @classmethod
    def find_movies(cls, es: Elasticsearch, movie_id_list: List[int]) -> List[Movies]:
        movies_search = cls.search(using=es)
        return movies_search.filter("terms", movieId=movie_id_list).execute().hits


    @classmethod
    def fuzzy_title(
        cls, es: Elasticsearch, title: str, fuzziness: Optional[int] = None,
        prefix_length: Optional[int] = None, max_expansions: Optional[int] = None) -> List[Movies]:
        movie_search = cls.search(using=es)
        return movie_search.query (Q({"fuzzy": {
            "title": {
                "value": title,
                **({"fuzziness": fuzziness} if fuzziness is not None else {}),
                **({"prefix_length": prefix_length} if prefix_length is not None else {}),
                **({"max_expansions": max_expansions} if max_expansions is not None else {})
            }
        }})).execute().hits



if __name__ == "__main__":
    es =  Elasticsearch(
        hosts=["https://localhost:9200"],
        http_auth=("admin", "admin"),
        verify_certs=False,
        use_ssl=True,
        ssl_show_warn=False,
    )

    movie = "Godfather"
    fuzzy = 50
    prefix_length = 100
    max_expansions = 100
    result = Movies().fuzzy_title(es=es, title=movie, fuzziness=fuzzy)
    for m in result:
        print(m.title)
                #,
