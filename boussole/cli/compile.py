# -*- coding: utf-8 -*-
import os
import click

import six

from boussole.conf.json_backend import SettingsBackendJson
from boussole.exceptions import BoussoleBaseException, SettingsBackendError
from boussole.finder import ScssFinder
from boussole.compiler import SassCompileHelper


@click.command('watch', short_help='Compile SASS project sources to CSS.')
@click.option('--config', default=None, metavar='PATH',
              help='Path to a Boussole config file',
              type=click.Path(exists=True))
@click.pass_context
def compile_command(context, config):
    """
    Compile SASS project sources to CSS
    """
    logger = context.obj['logger']
    logger.info(u"Building project")

    # Load settings file
    try:
        backend = SettingsBackendJson(basedir=os.getcwd())
        settings = backend.load(filepath=config)
    except SettingsBackendError as e:
        logger.critical(six.text_type(e))
        raise click.Abort()

    logger.debug(u"Project sources directory: {}".format(
                settings.SOURCES_PATH))
    logger.debug(u"Project destination directory: {}".format(
                settings.TARGET_PATH))
    logger.debug(u"Exclude patterns: {}".format(
                settings.EXCLUDES))

    # Find all sources with their destination path
    try:
        compilable_files = ScssFinder().mirror_sources(
            settings.SOURCES_PATH,
            targetdir=settings.TARGET_PATH,
            excludes=settings.EXCLUDES
        )
    except BoussoleBaseException as e:
        logger.error(six.text_type(e))
        raise click.Abort()

    # Build all compilable stylesheets
    compiler = SassCompileHelper()
    errors = 0
    for src, dst in compilable_files:
        logger.debug(u"Compile: {}".format(src))

        output_opts = {}
        success, message = compiler.safe_compile(settings, src, dst)

        if success:
            logger.info(u"Output: {}".format(message), **output_opts)
        else:
            errors += 1
            logger.error(message)

    # Ensure correct exit code if error has occured
    if errors:
        raise click.Abort()
