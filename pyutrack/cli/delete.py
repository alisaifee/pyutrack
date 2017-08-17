import click
from click import get_current_context

from pyutrack import *
from . import cli


@cli.group()
@click.pass_context
def delete(_):
    """
    delete youtrack resources
    """
    pass


@delete.resultcallback()
def result(result):
    get_current_context().obj.render(result)


@delete.command()
@click.pass_context
@click.argument('id')
def issue(ctx, id):
    return Issue(ctx.obj.connection, id=id).delete()


@delete.command()
@click.pass_context
@click.argument('id')
def project(ctx, id):
    return Project(ctx.obj.connection, id=id).delete()


@delete.command()
@click.pass_context
@click.argument('login')
def user(ctx, login):
    return User(ctx.obj.connection, login=login).delete()


@delete.command()
@click.pass_context
@click.argument('name')
def group(ctx, name):
    return Group(ctx.obj.connection, name=name).delete()
