from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Document, Float, Integer, Keyword, Text


@dataclass
class AvgRating:
    movie_id: int
    avg_rating: float
    votes: int


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

    @classmethod
    def top_rated_movies(
        cls, es: Elasticsearch, genre: Optional[str], votes: Optional[int]
    ) -> List[AvgRating]:
        default_votes = 10
        votes = votes or default_votes

        s = cls.search(using=es)
        if genre is not None:
            s = s.filter("term", **{"genres.keyword": genre})
        bucket_name = "top_rated"
        s.aggs.bucket(
            "top_rated",
            "terms",
            field="movieId",
            order={"avg_rating": "desc"},
            min_doc_count=f"{votes}",
            size="10000",
        ).metric("avg_rating", "avg", field="rating")

        top_10: List[Dict] = s.execute().aggregations[bucket_name]["buckets"][:10]
        return [
            AvgRating(
                movie_id=bucket["key"],
                avg_rating=bucket["avg_rating"]["value"],
                votes=bucket["doc_count"],
            )
            for bucket in top_10
        ]
