# -*- coding: utf-8 -*-
import click


@click.command()
@click.pass_context
def watch_command(context):
    """
    Watch for change on your project Sass stylesheets then compile them to CSS.
    """
    click.echo("Not implemented yet!")
