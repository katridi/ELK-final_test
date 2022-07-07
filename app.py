import json
from typing import Dict

import click

from app_context import create_app_context
from commands import match_term


@click.command()
@click.pass_context
@click.option("--term", default="customer_first_name.keyword", help="term for quering")
@click.option("--value", help="value for the term")
def match(ctx, term, value):
    query: Dict = match_term(term=term, value=value)
    res = ctx.obj.es.search(index=ctx.obj.index, body=query)
    print(json.dumps(res, indent=4, ensure_ascii=False))


@click.group()
@click.pass_context
def cli(ctx):
    pass


if __name__ == "__main__":
    cli.add_command(match)
    # make decorator to pass es
    app_context = create_app_context()
    cli(obj=app_context)