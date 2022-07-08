import json
import sys
from typing import Dict

import click

from app_context import create_app_context
from commands import match_term, fuzzy_term


@click.command()
@click.pass_context
@click.option("--term", default="customer_first_name.keyword", help="term for quering")
@click.option("--value", help="value for the term")
def match(ctx, term, value):
    query: Dict = match_term(term=term, value=value)
    res = ctx.obj.es.search(index=ctx.obj.index, body=query)
    print(json.dumps(res, indent=4, ensure_ascii=False))


@click.command()
@click.pass_context
@click.option("--term", default="customer_first_name.keyword", help="term for quering")
@click.option("--value", help="value for the term")
def fuzzy(ctx, term, value):
    query: Dict = fuzzy_term(term=term, value=value)
    res = ctx.obj.es.search(index=ctx.obj.index, body=query)
    print(json.dumps(res, indent=4, ensure_ascii=False))


@click.command()
@click.argument("raw_data", type=click.File('r'), default=sys.stdin)
@click.pass_context
def raw(ctx, raw_data):
    query: Dict = json.loads(raw_data.read())
    res = ctx.obj.es.search(index=ctx.obj.index, body=query)
    print(json.dumps(res, indent=4, ensure_ascii=False))


@click.group()
@click.pass_context
def cli(ctx):
    pass


if __name__ == "__main__":
    cli.add_command(match)
    cli.add_command(raw)
    cli.add_command(fuzzy)
    # make decorator to pass es
    app_context = create_app_context()
    cli(obj=app_context)
