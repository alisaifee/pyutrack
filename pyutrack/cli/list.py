import click
from click import get_current_context

from pyutrack import Issue, Project, User, Group
from . import cli


@cli.group()
@click.pass_context
def list(ctx):
    pass

@list.resultcallback()
def result(result):
    get_current_context().obj.render(result)

@list.command()
@click.pass_context
@click.option('--project', default=None)
@click.option('--filter', default=None)
def issues(ctx, project, filter):
    if project:
        return Project(ctx.obj.connection, id=project).issues()
    return Issue.list(ctx.obj.connection, filter=filter)

@list.command()
@click.pass_context
def projects(ctx):
    return Project.list(ctx.obj.connection)


@list.command()
@click.pass_context
def users(ctx):
    return User.list(ctx.obj.connection)


@list.command()
@click.pass_context
def groups(ctx):
    return Group.list(ctx.obj.connection)
