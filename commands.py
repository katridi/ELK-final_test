from typing import List

from elasticsearch import Elasticsearch
from elastic_schemas.user_ratings import UserRatings



def find_user_top(es: Elasticsearch, user_id: int) -> None:
    top_range = 5

    user_ratings_search = UserRatings.search(using=es)
    user_ratings = user_ratings_search.query('match', **{'userId': user_id})
    top_movies: List[UserRatings] = user_ratings.filter('range', rating={'gte': top_range}).execute().hits

    if not top_movies:
        print(F'For user with id="{user_id}" not found any movies with 5 star rating')
        return
    print(f'5 stars movies for user with id="{user_id}" are: ')
    for user in top_movies:
        print(user.title_and_year_id())
