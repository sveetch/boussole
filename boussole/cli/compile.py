# -*- coding: utf-8 -*-
import click

from boussole import __version__

@click.command()
@click.pass_context
def compile_command(context):
    """
    Compile Sass stylesheets to CSS 
    """
    click.echo("Not implemented yet!")
