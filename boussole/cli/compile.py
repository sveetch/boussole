# -*- coding: utf-8 -*-
import click
import logging
import os

import six

from boussole.compiler import SassCompileHelper
from boussole.conf.discovery import Discover
from boussole.conf.json_backend import SettingsBackendJson
from boussole.conf.yaml_backend import SettingsBackendYaml
from boussole.exceptions import BoussoleBaseException
from boussole.finder import ScssFinder
from boussole.project import ProjectBase


@click.command('watch', short_help='Compile Sass project sources to CSS.')
@click.option('--backend', metavar='STRING',
              type=click.Choice(['json', 'yaml']),
              help="Settings format name",
              default="json")
@click.option('--config', default=None, metavar='PATH',
              help='Path to a Boussole config file',
              type=click.Path(exists=True))
@click.pass_context
def compile_command(context, backend, config):
    """
    Compile Sass project sources to CSS
    """
    logger = logging.getLogger("boussole")
    logger.info(u"Building project")

    # Discover settings file
    try:
        discovering = Discover(backends=[SettingsBackendJson,
                                         SettingsBackendYaml])
        config_filepath, config_engine = discovering.search(
            filepath=config,
            basedir=os.getcwd(),
            kind=backend
        )

        project = ProjectBase(backend_name=config_engine._kind_name)
        settings = project.backend_engine.load(filepath=config_filepath)
    except BoussoleBaseException as e:
        logger.critical(six.text_type(e))
        raise click.Abort()

    logger.debug(u"Settings file: {} ({})".format(
                 config_filepath, config_engine._kind_name))
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
