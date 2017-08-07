import logging

import click
from requests import RequestException

from pyutrack import Credentials, Connection
from pyutrack.config import Config
from pyutrack.errors import ApiError, LoginError, ResponseError


@click.group()
@click.option('--base_url')
@click.option('--username')
@click.option('--password')
@click.option('--debug/--no-debug')
@click.pass_context
def cli(ctx, base_url, username, password, debug):
    """YouTrack CLI"""
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    if base_url:
        ctx.obj.api_url = base_url

    if username and username != ctx.obj.credentials.username:
        ctx.obj.credentials = Credentials(username, password)

    if not (ctx.obj.credentials.cookies or ctx.obj.credentials.password):
        ctx.obj.credentials.password = click.prompt(
            "Enter password for %s" % ctx.obj.credentials.username,
            hide_input=True
        )

    if not ctx.obj.credentials.cookies:
        ctx.obj.login()

    if base_url:
        ctx.obj.api_url = base_url


from pyutrack.cli import new, show, update, delete, list


def main():
    config = Config()
    connection = Connection(credentials=config.credentials)
    if config.base_url:
        connection.api_url = config.base_url
    try:
        cli(obj=connection, auto_envvar_prefix='YOUTRACK')
    except (ApiError, LoginError, ResponseError) as e:
        click.secho(str(e), fg='red')
    except (RequestException,) as e:
        click.secho(str(e), fg='red')