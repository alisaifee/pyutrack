import click
from click import get_current_context

from pyutrack import *
from pyutrack.cli import update
from pyutrack.cli.util import admin_command
from pyutrack.config import Config
from pyutrack.errors import LoginError
from . import cli


@cli.group()
@click.pass_context
def new(_):
    """
    create new youtrack resources
    """
    pass


@new.resultcallback()
def result(result):
    get_current_context().obj.render(result)


@new.command()
@click.pass_context
@click.argument('project')
@click.argument('summary')
@click.option('--description', help='issue details')
@click.option('--command', help='command to run after issue is created')
def issue(ctx, project, summary, description, command):
    """create a new issue"""
    issue = Issue.create(
        ctx.obj.connection,
        project=project,
        summary=summary,
        description=description
    )
    if command:
        issue.command(command)
    return issue


@new.command()
@click.pass_context
@click.argument('id')
@click.argument('name')
@click.option(
    '--lead',
    default=lambda: get_current_context().obj.connection.credentials.username
)
@admin_command
def project(ctx, id, name, lead):
    """create a new project"""
    return Project.create(ctx.obj.connection, name, lead, project_id=id)


@new.command()
@click.pass_context
@click.argument('login')
@click.argument('name')
@click.argument('email')
@click.argument('password')
@click.option('--group', multiple=True, help='group(s) to add new user to')
@admin_command
def user(ctx, login, name, email, password, group):
    """create a new user"""
    user = User.create(ctx.obj.connection, login, name, email, password)
    user.groups += group
    return user


@new.command()
@click.pass_context
@click.argument('name')
@click.option('--description')
@click.option('--auto-join/--no-auto-join', help='automatically add new users')
#@click.option('--role', multiple=True, help='role(s) to give new group')
@admin_command
def group(ctx, name, description, auto_join):
    """create a new group"""
    group = Group.create(
        ctx.obj.connection, name, description=description, auto_join=auto_join
    )
    #if role:
    #    group.roles += role
    return group


@new.command()
@click.pass_context
@click.argument('name')
@click.option('--description')
@click.option(
    '--permission', multiple=True, help='permission(s) to give new role'
)
@admin_command
def role(ctx, name, description, permission):
    """create a new role"""
    role = Role.create(ctx.obj.connection, name, description=description)
    if permission:
        role.permissions += permission


@new.command()
@click.pass_context
@click.option('--force', type=click.BOOL, default=False)
@click.option('--path', default=Config.DEFAULT_PATH)
def config(ctx, force, path, base_url=None, username=None):
    """
    generate a new config
    """
    cfg = Config(path)
    if not cfg.persisted or force or click.prompt(
        'This will overwrite the current configuration', type=bool
    ):
        cfg.base_url = click.prompt(
            "Enter base url for youtrack", default=base_url
        )
        username = click.prompt("Enter username", default=username)
        password = click.prompt(
            "Enter password for %s" % username, hide_input=True
        )
        credentials = Credentials(username, password)
        cfg.credentials = credentials
        try:
            Connection(cfg.base_url, credentials).login()
            cfg.persist()
            credentials.persist()
            click.secho('Configuration saved', fg='green')
        except (Exception, ) as e:  # noqa
            print(e)
            if click.prompt(
                click.style(
                    "Verification failed. Would you like to try again?",
                    fg='red'
                ),
                type=bool
            ):
                ctx.invoke(
                    config,
                    force=True,
                    base_url=cfg.base_url,
                    username=credentials.username
                )
