import click
from click import get_current_context
from pyutrack import *
from . import cli


@cli.group()
@click.pass_context
def list(ctx):
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
    if project:
        return Project(
            ctx.obj.connection, id=project
        ).get_issues(
            filter=filter, max=limit
        )
    return Issue.list(ctx.obj.connection, filter=filter, max=limit)


@list.command()
@click.pass_context
def projects(ctx):
    return Project.list(ctx.obj.connection)


@list.command()
@click.pass_context
@click.option('--group', default='')
@click.option('--role', default='')
@click.option('--query', default='')
@click.option('--permission', default='')
@click.option('--project', default='')
def users(ctx, query, group, role, permission, project):
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
@click.option('--user', default=None)
def groups(ctx, user):
    if user:
        return User(ctx.obj.connection, login=user).groups
    return Group.list(ctx.obj.connection)


@list.command()
@click.pass_context
@click.option('--group', default=None)
@click.option('--user', default=None)
def roles(ctx, group, user):
    if group:
        return Group(ctx.obj.connection, name=group).roles
    if user:
        return User(ctx.obj.connection, login=user).roles
    return Role.list(ctx.obj.connection)


@list.command()
@click.pass_context
@click.option('--role', default=None)
def permissions(ctx, role):
    if role:
        return Role(ctx.obj.connection, name=role).permissions
    return Permission.list(ctx.obj.connection)


@list.command()
@click.pass_context
@click.option('--issue', default=None)
def links(ctx, issue):
    if issue:
        return Issue(ctx.obj.connection, id=issue).issue_links
    # lol
    return IssueLinkType.list(ctx.obj.connection)
