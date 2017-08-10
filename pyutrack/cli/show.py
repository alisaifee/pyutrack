import click
from click import get_current_context

from pyutrack import *
from . import cli

@cli.group()
@click.pass_context
def show(ctx):
    pass

@show.resultcallback()
def result(result):
    get_current_context().obj.render(result)

@show.command()
@click.pass_context
@click.argument('id')
def issue(ctx, id):
    return Issue(ctx.obj.connection, hydrate=True, id=id)


@show.command()
@click.pass_context
@click.argument('id')
def project(ctx, id):
    return Project(ctx.obj.connection, hydrate=True, id=id)


@show.command()
@click.pass_context
@click.argument('login')
def user(ctx, login):
    return User(ctx.obj.connection, hydrate=True, login=login)


@show.command()
@click.pass_context
@click.argument('name')
def group(ctx, name):
    return Group(ctx.obj.connection, hydrate=True, name=name)
