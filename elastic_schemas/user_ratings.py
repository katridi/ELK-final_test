from __future__ import annotations

from typing import List

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Document, Float, Integer, Keyword, Text


class UserRatings(Document):
    user_id = Integer()
    movieId = Integer()
    rating = Float()
    title = Text()
    genres = Keyword()
    year = Integer()
    _top_range = 5

    class Index:
        name = "user_ratings"
        settings = {
            "refresh_interval": "1",
            "number_of_shards": "1",
        }

    def title_and_year(self) -> str:
        return f"| {self.title} | {self.year} |"

    @classmethod
    def user_top_movies(cls, es: Elasticsearch, user_id: int) -> List[UserRatings]:
        user_ratings_search = cls.search(using=es)
        user_ratings = user_ratings_search.query("match", **{"userId": user_id})
        top_movies: List[UserRatings] = (
            user_ratings.filter("range", rating={"gte": cls._top_range}).execute().hits
        )
        return top_movies
