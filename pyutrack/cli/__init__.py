import logging

import click

from pyutrack import Credentials


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
        print("but why")
        ctx.obj.login()

    if base_url:
        ctx.obj.api_url = base_url


from . import new, show, update, delete, list
