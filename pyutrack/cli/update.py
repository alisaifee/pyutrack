import click
from click import get_current_context

from pyutrack import Issue, User, Group, Role
from pyutrack.cli.util import admin_command
from pyutrack.errors import InputError, CliError
from . import cli


@cli.group()
@click.pass_context
def update(_):
    """
    update existing youtrack resources
    """
    pass


@update.resultcallback()
def result(result):
    get_current_context().obj.render(result)


@update.command()
@click.pass_context
@click.argument('id')
@click.option('--summary')
@click.option('--description')
@click.option('--command', help='command to apply to issue.')
def issue(ctx, id, summary, description, command):
    """update an issue"""
    issue = Issue(ctx.obj.connection, hydrate=False, id=id)
    if command:
        issue.command(command)
    else:
        issue.update(summary=summary, description=description)
    return issue


@update.command()
@click.pass_context
@click.argument('login')
@click.option('--name', default=None)
@click.option('--email', default=None)
@click.option('--password', default=None)
@click.option('add_groups', '+group', multiple=True, help='add user to group')
@click.option(
    'remove_groups', '-group', multiple=True, help='remove user from group'
)
#@click.option('add_roles', '+role', multiple=True, help='add role to user')
#@click.option(
#    'remove_roles', '-role', multiple=True, help='remove role from user'
#)
@admin_command
def user(ctx, login, name, email, password, add_groups, remove_groups):
    """update a user"""
    user = User(ctx.obj.connection, hydrate=True, login=login)
    if name or email or password:
        user.update(full_name=name, email=email, password=password)
    user.groups += add_groups
    user.groups -= remove_groups
    #user.roles += add_roles
    #user.roles -= remove_roles
    return user


@update.command()
@click.pass_context
@click.argument('name')
# TODO: rest api for adding roles to groups is returning a 500
# #@click.option('add_roles', '+role', multiple=True)
# @click.option('remove_roles', '-role', multiple=True)
@admin_command
def group(ctx, name):
    """update a group"""
    group = Group(ctx.obj.connection, hydrate=True, name=name)
    return group
    # group.roles += add_roles
    # group.roles -= remove_roles


@update.command()
@click.pass_context
@click.argument('name')
@click.option(
    'add_permissions', '+permission', multiple=True, help='add permission'
)
@click.option(
    'remove_permissions',
    '-permission',
    multiple=True,
    help='remove permission'
)
@admin_command
def role(ctx, name, add_permissions, remove_permissions):
    """update a role"""
    role = Role(ctx.obj.connection, hydrate=False, name=name)
    role.permissions += add_permissions
    role.permissions -= remove_permissions
