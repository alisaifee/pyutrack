import click
from click import get_current_context

from pyutrack import *
from pyutrack.cli.util import admin_command
from . import cli


@cli.group()
@click.pass_context
def show(_):
    """
    show details for youtrack resources
    """
    pass


@show.resultcallback()
def result(result):
    get_current_context().obj.render(result)


@show.command()
@click.pass_context
@click.argument('id')
def issue(ctx, id):
    """show issue details"""
    return Issue(ctx.obj.connection, hydrate=True, id=id)


@show.command()
@click.pass_context
@click.argument('id')
@admin_command
def project(ctx, id):
    """show project details"""
    return Project(ctx.obj.connection, hydrate=True, id=id)


@show.command()
@click.pass_context
@click.argument('login')
@admin_command
def user(ctx, login):
    """show user details"""
    return User(ctx.obj.connection, hydrate=True, login=login)


@show.command()
@click.pass_context
@click.argument('name')
@admin_command
def group(ctx, name):
    """show group details"""
    return Group(ctx.obj.connection, hydrate=True, name=name)


@show.command()
@click.pass_context
@click.argument('name')
@admin_command
def role(ctx, name):
    """show role details"""
    return Role(ctx.obj.connection, name=name)


@show.command()
@click.pass_context
def config(ctx):
    """show current cli configuration"""
    click.echo(
        """Base url: %(base_url)s
username: %(username)s""" % {
            'base_url': ctx.obj.connection.api_url,
            'username': ctx.obj.connection.credentials.username
        }
    )
