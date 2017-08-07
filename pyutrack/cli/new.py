import click

from . import cli


@cli.group()
@click.pass_context
def new(ctx):
    pass


@new.command()
@click.pass_context
def issue(ctx):
    print(ctx.obj.api_url)


@new.command()
@click.pass_context
def project(ctx):
    print(ctx.obj)


@new.command()
@click.pass_context
def user(ctx):
    print(ctx.obj)


@new.command()
@click.pass_context
def group(ctx):
    print(ctx.obj)
