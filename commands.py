from typing import List, Optional

from elasticsearch import Elasticsearch

from elastic_schemas.movies import Movies
from elastic_schemas.user_ratings import AvgRating, UserRatings
from rich_print.tables import TopMoviesConsoleTable, MovieTagsTable, MovieTable


def find_user_top(es: Elasticsearch, user_id: int) -> None:
    top_movies: List[UserRatings] = UserRatings.user_top_movies(es=es, user_id=user_id)
    if not top_movies:
        print(f'For user with id="{user_id}" not found any movies with 5 star rating')
        return
    print(f'\n5 stars movies for user with id="{user_id}" are: ')
    table = MovieTable()
    for user in top_movies:
        row = [user.title, user.year, user.genres[:5]]
        table.populate_row(row)
    table.print()


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
    table = MovieTagsTable()
    for tag, relevance in zip(movie.tag, movie.relevance):
        table.populate_row(row=[tag, round(relevance, 2)])
    table.print()


def find_top_10_rated_movies(es: Elasticsearch, genre: Optional[str], votes: Optional[int]) -> None:
    avg_rating_list: List[AvgRating] = UserRatings.top_rated_movies(es=es, genre=genre, votes=votes)
    table = TopMoviesConsoleTable()
    # TO preserve the order
    for index, item in enumerate(avg_rating_list, 1):
        movie: List[Movies] = Movies.find_movies(es=es, movie_id_list=[item.movie_id])[0]
        row = [index, movie.title, movie.year, round(item.avg_rating, 2), movie.genres[:3], item.votes, movie.imdbId]
        table.populate_row(row=row)
    table.print()


def fuzzy_search_movies(
    es: Elasticsearch,
    title: str,
    fuzziness: Optional[int] = None,
    prefix_length: Optional[int] = None,
    max_expansions: Optional[int] = None,
) -> None:
    movies: List[Movies] = Movies.fuzzy_title(
        es=es, title=title, fuzziness=fuzziness, prefix_length=prefix_length, max_expansions=max_expansions
    )
    if not movies:
        print("There are no movies found, try to adjust params")
        return
    table = MovieTable()
    for movie in movies:
        row = [movie.title, movie.year, movie.genres[:3]]
        table.populate_row(row=row)
    table.print()


def match_movie_title(es: Elasticsearch, title: str) -> None:
    movies: List[Movies] = Movies.match_title(es=es, title=title)
    print("There are no movies found, try to adjust title")
    table = MovieTable()
    for movie in movies:
        row = [movie.title, movie.year, movie.genres[:3]]
        table.populate_row(row=row)
    table.print()