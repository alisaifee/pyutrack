import click
from click import get_current_context

from pyutrack import Issue, Project, User, Group, Role
from . import cli


@cli.group()
@click.pass_context
def update(ctx):
    pass


@update.resultcallback()
def result(result):
    get_current_context().obj.render(result)


@update.command()
@click.pass_context
@click.argument('id')
@click.option('--summary')
@click.option('--description')
@click.option('--command')
def issue(ctx, id, summary, description, command):
    issue = Issue(ctx.obj.connection, hydrate=False, id=id)
    if command:
        issue.command(command)
    else:
        issue.update(summary=summary, description=description)
    return issue


@update.command()
@click.pass_context
@click.argument('id')
def project(ctx, id):
    return Project(ctx.obj.connection, hydrate=True, id=id)


@update.command()
@click.pass_context
@click.argument('login')
@click.option('add_groups', '+group', multiple=True)
@click.option('remove_groups', '-group', multiple=True)
def user(ctx, login, add_groups, remove_groups):
    user = User(ctx.obj.connection, hydrate=True, login=login)
    user.groups += add_groups
    user.groups -= remove_groups


@update.command()
@click.pass_context
@click.argument('name')
@click.option('add_roles', '+role', multiple=True)
@click.option('remove_roles', '-role', multiple=True)
def group(ctx, name, add_roles, remove_roles):
    group = Group(ctx.obj.connection, hydrate=True, name=name)
    group.roles += add_roles
    group.roles -= remove_roles


@update.command()
@click.pass_context
@click.argument('name')
@click.option('add_permissions', '+permission', multiple=True)
@click.option('remove_permissions', '-permission', multiple=True)
def role(ctx, name, add_permissions, remove_permissions):
    role = Role(ctx.obj.connection, hydrate=False, name=name)
    role.permissions += add_permissions
    role.permissions -= remove_permissions
