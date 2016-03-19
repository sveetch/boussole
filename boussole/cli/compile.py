# -*- coding: utf-8 -*-
import click


@click.command()
@click.pass_context
def compile_command(context):
    """
    Compile Sass stylesheets to CSS
    """
    click.echo("Not implemented yet!")
