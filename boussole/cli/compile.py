# -*- coding: utf-8 -*-
import os
import click
import sass

from boussole.exceptions import SettingsBackendError
from boussole.finder import ScssFinder
from boussole.utils import build_target_helper

from boussole.conf.json_backend import SettingsBackendJson


@click.command()
@click.option('--config', default=None, metavar='PATH',
              help='Path to a Boussole config file',
              type=click.Path(exists=True))
@click.pass_context
def compile_command(context, config):
    """
    Compile Sass stylesheets to CSS
    """
    click.echo("Build command")

    # Load settings file
    try:
        backend = SettingsBackendJson(basedir=os.getcwd())
        settings = backend.load(filepath=config)
    except SettingsBackendError as e:
        raise click.UsageError(e.message)

    click.echo("SOURCE DIR: {}".format(settings.SOURCES_PATH))
    click.echo("TARGET DIR: {}".format(settings.TARGET_PATH))
    click.echo("EXCLUDES: {}".format(settings.EXCLUDES))

    # Find all sources with destination path
    compile_map = ScssFinder().mirror_sources(
        settings.SOURCES_PATH,
        targetdir=settings.TARGET_PATH,
        excludes=settings.EXCLUDES
    )

    # Build all compilable stylesheets
    for src, dst in compile_map:
        click.echo("Building: {}".format(src))

        try:
            content = sass.compile(
                filename=src,
                output_style=settings.OUTPUT_STYLES,
                source_comments=settings.SOURCE_COMMENTS,
                include_paths=settings.LIBRARY_PATHS,
            )
        except sass.CompileError as e:
            click.secho(e.message, fg='red')
        else:
            build_target_helper(content, dst)
            click.echo("To: {}".format(dst))

        click.echo("---")
