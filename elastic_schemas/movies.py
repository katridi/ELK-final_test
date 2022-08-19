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
        name = 'movies'
        settings = {
          "refresh_interval" : "1",
          "number_of_shards" : "1",
        }

    @classmethod
    def find_movie(cls, es: Elasticsearch, movie_id: int) -> List[Movies]:
        movies_search = cls.search(using=es)
        return movies_search.query('match', **{'movieId': movie_id}).execute().hits
        


if __name__ == '__main__':
    from typing import List

    from elasticsearch import Elasticsearch

    es = Elasticsearch(
        hosts=["https://localhost:9200"],
        http_auth=("admin", "admin"),
        verify_certs=False,
        use_ssl=True,
        ssl_show_warn=False
    )
