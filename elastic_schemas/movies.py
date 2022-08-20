from __future__ import annotations

from typing import List

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Document, Float, Integer, Keyword, Text


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
