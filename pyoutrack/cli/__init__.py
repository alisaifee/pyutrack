import click

from pyoutrack import Credentials
from pyoutrack import Connection


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.option('--base_url')
@click.option('--username')
@click.option('--password')
@click.pass_context
def cli(ctx, debug, base_url, username, password):
    """YouTrack CLI"""
    credentials = Credentials(username, password)
    ctx.obj.credentials = credentials
    ctx.obj.api_url = base_url

from . import new, update, delete, list