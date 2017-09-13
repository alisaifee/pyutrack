import collections

import click
import six
import sys


def admin_command(fn):
    fn.__doc__ += ' [Admin only]'
    return fn


class PyutrackContext(object):
    def __init__(self, connection, config, debug=False):
        self.connection = connection
        self.config = config
        self.debug = debug
        self.format = None
        self.watch = None

    def render(self, data, format=None):
        format = self.format or format
        oneline = format == 'oneline'
        line_sep = '\n' if format else '\n\n'
        resp = ''
        if isinstance(data, six.string_types):
            resp = data
        elif isinstance(data, collections.Iterable):
            resp = line_sep.join(
                k.format(format, oneline=oneline) for k in data
            ) if len(data) > 0 else click.style(
                'No results', fg='yellow'
            )
        elif data:
            resp = data.format(format, oneline=oneline)
        if self.watch and self.watch > 0:
            click.clear()
            click.secho(
                "pyu watching command: %s, every %d seconds" % (
                    " ".join(sys.argv[1:]), self.watch
                ), fg='yellow'
            )
        click.echo(resp)
