import collections

import click


def admin_command(fn):
    fn.__doc__ += ' [Admin only]'
    return fn


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
        if isinstance(data, collections.Iterable):
            resp = line_sep.join(
                k.format(format, oneline=oneline) for k in data
            ) if len(data) > 0 else click.style(
                'No results', fg='yellow'
            )
        elif data:
            resp = data.format(format, oneline=oneline)
        click.echo(resp)
