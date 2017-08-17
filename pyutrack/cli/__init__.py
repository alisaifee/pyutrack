import collections
import logging

import click
from requests import RequestException

from pyutrack import Credentials, Connection
from pyutrack.config import Config
from pyutrack.errors import ApiError, LoginError, ResponseError, CliError


@click.group()
@click.option('--base_url', help='root url of your youtrack installation')
@click.option('--username', help='username to access youtrack as')
@click.option('--password', help='password for current user')
@click.option('--debug/--no-debug', help='enable/disable verbose logging')
@click.pass_context
def cli(ctx, base_url, username, password, debug):
    """
    YouTrack
    """
    connection = ctx.obj.connection
    ctx.obj.debug = debug
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    if base_url:
        connection.api_url = base_url

    if username and username != connection.credentials.username:
        connection.credentials = Credentials(username, password)
    if not connection.api_url or not connection.credentials.username:
        ctx.invoke(new.config)
        ctx.obj.config.reload()
        connection.api_url = ctx.obj.config.base_url
        connection.credentials = ctx.obj.config.credentials
    if not (connection.credentials.cookies or connection.credentials.password):
        connection.credentials.password = click.prompt(
            "Enter password for %s" % connection.credentials.username,
            hide_input=True
        )
    if not connection.credentials.cookies:
        connection.login()
    if base_url:
        connection.api_url = base_url


from pyutrack.cli import new, show, update, delete, list


class PyutrackContext(object):
    def __init__(self, connection, config, debug=False):
        self.connection = connection
        self.config = config
        self.debug = debug
        self.format = None

    def render(self, data, format=None):
        format = self.format or format
        oneline = format == 'oneline'
        line_sep = '\n' if format else '\n\n'
        if data:
            if isinstance(data, collections.Iterable):
                resp = line_sep.join(
                    k.format(format, oneline=oneline) for k in data
                )
            else:
                resp = data.format(format, oneline=oneline)
            click.echo(resp)


def main():
    config = Config()
    connection = Connection(credentials=config.credentials)
    if config.base_url:
        connection.api_url = config.base_url
    try:
        cli(
            obj=PyutrackContext(connection, config),
            auto_envvar_prefix='YOUTRACK'
        )
    except (ApiError, LoginError, ResponseError, CliError) as e:
        click.secho(str(e), fg='red')
    except (RequestException, CliError) as e:
        click.secho(str(e), fg='red')
