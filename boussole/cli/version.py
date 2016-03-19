# -*- coding: utf-8 -*-
import click

from boussole import __version__


@click.command()
@click.pass_context
def version_command(context):
    """
    Print out version information
    """
    click.echo("Boussole {}".format(__version__))
