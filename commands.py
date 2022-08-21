from typing import List, Optional

from elasticsearch import Elasticsearch

from elastic_schemas.movies import Movies
from elastic_schemas.user_ratings import AvgRating, UserRatings
from rich_print.tables import TopMoviesConsoleTable


def find_user_top(es: Elasticsearch, user_id: int) -> None:
    top_movies: List[UserRatings] = UserRatings.user_top_movies(es=es, user_id=user_id)
    if not top_movies:
        print(f'For user with id="{user_id}" not found any movies with 5 star rating')
        return
    print(f'5 stars movies for user with id="{user_id}" are: ')
    for user in top_movies:
        print(user.title_and_year())


def find_top_10_tags_for_movie_id(es: Elasticsearch, movie_id: int) -> None:
    movies: List[Movies] = Movies.find_movies(es=es, movie_id_list=[movie_id])

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


def find_top_10_rated_movies(es: Elasticsearch, genre: Optional[str], votes: Optional[int]) -> None:
    avg_rating_list: List[AvgRating] = UserRatings.top_rated_movies(
        es=es, genre=genre, votes=votes
    )
    table = TopMoviesConsoleTable()
    # TO preserve the order
    for index, item in enumerate(avg_rating_list, 1):
        movie: List[Movies] = Movies.find_movies(es=es, movie_id_list=[item.movie_id])[0]
        row = [index, movie.title, movie.year, round(item.avg_rating, 2), movie.genres[:3], item.votes, movie.imdbId]
        table.populate_row(row=row)
    table.print()
