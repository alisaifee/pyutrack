import click
from requests import RequestException

from pyutrack import Connection
from pyutrack.cli import cli
from pyutrack.config import Config
from pyutrack.errors import ApiError, LoginError, ResponseError

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
