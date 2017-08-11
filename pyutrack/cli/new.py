import click
from click import get_current_context

from pyutrack import *
from . import cli


@cli.group()
@click.pass_context
def new(ctx):
    pass


@new.resultcallback()
def result(result):
    get_current_context().obj.render(result)


@new.command()
@click.pass_context
@click.option('--project')
@click.argument('summary')
@click.argument('description')
def issue(ctx, project, summary, description):
    return Issue.create(
        ctx.obj.connection,
        project=project,
        summary=summary,
        description=description
    )


@new.command()
@click.pass_context
@click.argument('id')
@click.argument('name')
@click.argument('lead')
def project(ctx, id, name, lead):
    return Project.create(ctx.obj.connection, id, name, lead)


@new.command()
@click.pass_context
@click.argument('login')
@click.argument('name')
@click.argument('email')
@click.argument('password')
def user(ctx, login, name, email, password):
    return User.create(ctx.obj.connection, login, name, email, password)


@new.command()
@click.pass_context
@click.argument('name')
@click.option('--description')
@click.option('--auto-join/--no-auto-join')
def group(ctx, name, description, auto_join):
    return Group.create(
        ctx.obj.connection, name, description=description, auto_join=auto_join
    )


@new.command()
@click.pass_context
@click.argument('name')
@click.option('--description')
def role(ctx, name, description):
    return Role.create(ctx.obj.connection, name, description=description)
