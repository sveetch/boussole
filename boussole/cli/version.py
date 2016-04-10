# -*- coding: utf-8 -*-
import click

from sass import __version__ as libsasspython_version
from _sass import libsass_version
from boussole import __version__


@click.command()
@click.pass_context
def version_command(context):
    """
    Print out version information.
    """
    click.echo("Boussole {} (libsass-python {}) (libsass {})".format(
        __version__,
        libsasspython_version,
        libsass_version,
    ))
