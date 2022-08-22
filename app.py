from typing import Optional

import click

from app_context import AppContext, create_app_context
from commands import (
    find_top_10_rated_movies,
    find_top_10_tags_for_movie_id,
    find_user_top,
    fuzzy_search_movies
)


@click.command()
@click.pass_context
@click.argument("user_id", type=int)
def user_top(ctx, user_id: int) -> None:
    """Takes user_id and output in std top movies"""
    app_ctx: AppContext = ctx.obj
    find_user_top(es=app_ctx.es, user_id=user_id)


@click.command()
@click.pass_context
@click.argument("movie_id", type=int)
def movie_tags(ctx, movie_id: int) -> None:
    """Takes movie_id and output in top10 tags"""
    app_ctx: AppContext = ctx.obj
    find_top_10_tags_for_movie_id(es=app_ctx.es, movie_id=movie_id)


@click.command()
@click.pass_context
@click.option("--genre", type=str, help="to filter rating by genre")
@click.option("--votes", type=int, help="to filter rating by minimum votes given")
def top_movies(ctx, genre: Optional[str], votes: Optional[int]) -> None:
    """Output top rated movies, addionally filters by genres and min votes"""
    app_ctx: AppContext = ctx.obj
    find_top_10_rated_movies(es=app_ctx.es, genre=genre, votes=votes)


@click.command()
@click.pass_context
@click.argument("title", type=str)
@click.option("--fuzziness", type=int, help="maximum edit distance allowed for matching")
@click.option("--prefix_length", type=int, help="number of beginning characters left unchanged when creating expansions")
@click.option("--max_expansions", type=int, help="maximum number of variations created")
def fuzzy(ctx, title: str, fuzziness: Optional[int], prefix_length: Optional[int], max_expansions: Optional[int]) -> None:
    """Fuzzy search movie titles"""
    app_ctx: AppContext = ctx.obj
    fuzzy_search_movies(
        es=app_ctx.es, title=title, fuzziness=fuzziness,
        prefix_length=prefix_length, max_expansions=max_expansions
    )




@click.group()
@click.pass_context
def cli(ctx):
    pass


if __name__ == "__main__":
    commands = [user_top, movie_tags, top_movies, fuzzy]
    for command in commands:
        cli.add_command(command)
    app_context = create_app_context()
    cli(obj=app_context)
