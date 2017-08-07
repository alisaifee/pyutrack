import click

from pyutrack import Issue, Project, User, Group
from . import cli


@cli.group()
@click.pass_context
def list(ctx):
    pass


@list.command()
@click.pass_context
@click.option('--project')
def issues(ctx, project=None):
    if project:
        click.echo(Project(ctx.obj, id=project).issues())


@list.command()
@click.pass_context
def projects(ctx):
    click.echo(Project.list(ctx.obj))


@list.command()
@click.pass_context
def users(ctx):
    click.echo(User.list(ctx.obj))


@list.command()
@click.pass_context
def groups(ctx):
    click.echo(Group.list(ctx.obj))
