import click

from pyutrack import Issue
from . import cli


@cli.group()
@click.pass_context
def show(ctx):
    pass


@show.command()
@click.pass_context
@click.argument('id')
def issue(ctx, id):
    print(Issue(ctx.obj, hydrate=True, id=id))


@show.command()
@click.pass_context
def project(ctx):
    print(ctx.obj)


@show.command()
@click.pass_context
def user(ctx):
    print(ctx.obj)


@show.command()
@click.pass_context
def group(ctx):
    print(ctx.obj)
