from typing import List

from elasticsearch import Elasticsearch
from elastic_schemas.user_ratings import UserRatings
from elastic_schemas.movies import Movies


def find_user_top(es: Elasticsearch, user_id: int) -> None:
    top_movies: List[UserRatings] = UserRatings.user_top_movies(es=es, user_id=user_id)
    if not top_movies:
        print(f'For user with id="{user_id}" not found any movies with 5 star rating')
        return
    print(f'5 stars movies for user with id="{user_id}" are: ')
    for user in top_movies:
        print(user.title_and_year())


def find_top_10_tags_for_movie_id(es: Elasticsearch, movie_id: int) -> None:
    movies: List[Movies] = Movies.find_movie(es=es, movie_id=movie_id)

    if not movies:
        print(f'There is no movie with id="{movie_id}"')
        return

    # we imply unique id for movies
    movie = movies[0]
    if not movie.tag:
        print(f'Movie id="{movie.movieId}" "{movie.title}" there are no tags:')
        return
    print(f'Movie id="{movie.movieId}" "{movie.title}" top10 tags are:')
    [print(f"| {x} |") for x in movie.tag]
