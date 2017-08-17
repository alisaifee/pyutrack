import click
from click import get_current_context
from pyutrack import *
from pyutrack.cli.util import admin_command
from . import cli


@cli.group()
@click.pass_context
def list(_):
    """
    List various youtrack resources
    """
    pass


@list.resultcallback()
def result(result):
    get_current_context().obj.render(result)


@list.command()
@click.pass_context
@click.option('--project', default=None)
@click.option('--filter', default='')
@click.option('--limit', default=100)
def issues(ctx, project, filter, limit):
    """list issues"""
    if project:
        return Project(
            ctx.obj.connection, id=project
        ).get_issues(
            filter=filter, max=limit
        )
    return Issue.list(ctx.obj.connection, filter=filter, max=limit)


@list.command()
@click.pass_context
@admin_command
def projects(ctx):
    """list projects"""
    return Project.list(ctx.obj.connection)


@list.command()
@click.pass_context
@click.option('--group', default='', help='group name')
@click.option('--role', default='', help='role name')
@click.option('--query', default='', help='query to match users against')
@click.option('--permission', default='', help='permission name')
@click.option('--project', default='')
@admin_command
def users(ctx, query, group, role, permission, project):
    """
    list users
    """
    return User.list(
        ctx.obj.connection,
        query=query,
        group=group,
        role=role,
        permission=permission,
        project=project
    )


@list.command()
@click.pass_context
@click.option('--user', default=None, help='user login')
@admin_command
def groups(ctx, user):
    """
    list groups
    """
    if user:
        return User(ctx.obj.connection, login=user).groups
    return Group.list(ctx.obj.connection)


@list.command()
@click.pass_context
@click.option('--group', default=None, help='group name')
@click.option('--user', default=None, help='user login')
@admin_command
def roles(ctx, group, user):
    """
    list roles
    """
    if group:
        return Group(ctx.obj.connection, name=group).roles
    if user:
        return User(ctx.obj.connection, login=user).roles
    return Role.list(ctx.obj.connection)


@list.command()
@click.pass_context
@click.option('--role', default=None, help='role name')
@admin_command
def permissions(ctx, role):
    """
    list permissions
    """
    if role:
        return Role(ctx.obj.connection, name=role).permissions
    return Permission.list(ctx.obj.connection)


@list.command()
@click.pass_context
@click.option('--issue', default=None, help='issue id')
def links(ctx, issue):
    """
    list issue links
    """
    if issue:
        return Issue(ctx.obj.connection, id=issue).issue_links
    # lol
    return IssueLinkType.list(ctx.obj.connection)
