# -*- coding: utf-8 -*-
import os
import click
import sass

from boussole.conf.json_backend import SettingsBackendJson
from boussole.exceptions import SettingsBackendError
from boussole.finder import ScssFinder
from boussole.utils import build_target_helper


@click.command()
@click.option('--config', default=None, metavar='PATH',
              help='Path to a Boussole config file',
              type=click.Path(exists=True))
@click.pass_context
def compile_command(context, config):
    """
    Compile Sass stylesheets to CSS
    """
    logger = context.obj['logger']
    click.secho("Building project", fg='green')

    # Load settings file
    try:
        backend = SettingsBackendJson(basedir=os.getcwd())
        settings = backend.load(filepath=config)
    except SettingsBackendError as e:
        logger.error(e.message)
        raise click.Abort()

    logger.info("Project sources directory: {}".format(settings.SOURCES_PATH))
    logger.info("Project destination directory: {}".format(settings.TARGET_PATH))
    logger.info("Exclude patterns: {}".format(settings.EXCLUDES))

    # Find all sources with their destination path
    compilable_files = ScssFinder().mirror_sources(
        settings.SOURCES_PATH,
        targetdir=settings.TARGET_PATH,
        excludes=settings.EXCLUDES
    )

    # Build all compilable stylesheets
    for src, dst in compilable_files:
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

        click.echo("")
