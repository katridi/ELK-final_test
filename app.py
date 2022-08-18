import click

from app_context import AppContext, create_app_context
from commands import find_user_top, find_top_10_tags_for_movie_id


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


@click.group()
@click.pass_context
def cli(ctx):
    pass


if __name__ == "__main__":
    commands = [user_top, movie_tags]
    for command in commands:
        cli.add_command(command)
    app_context = create_app_context()
    cli(obj=app_context)