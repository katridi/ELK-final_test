from elasticsearch_dsl import Document, Integer, Keyword, Text, Float


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


if __name__ == '__main__':
    from elasticsearch import Elasticsearch
    from typing import List

    es = Elasticsearch(
        hosts=["https://localhost:9200"],
        http_auth=("admin", "admin"),
        verify_certs=False,
        use_ssl=True,
        ssl_show_warn=False
    )
    movie_id = 904

    movies_search = Movies.search(using=es)
    movies: List[Movies] = movies_search.query('match', **{'movieId': movie_id}).execute().hits

    for movie in movies:
        if not movie.tag:
            print(F'Movie id="{movie.movieId}" "{movie.title}" there are no tags:')
            continue    
        print(F'Movie id="{movie.movieId}" "{movie.title}" top10 tags are:')
        [print(f'{x}', sep=' | ', end='') for x in movie.tag]