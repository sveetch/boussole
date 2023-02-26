# -*- coding: utf-8 -*-
import click
import logging
import os

from ..compiler import SassCompileHelper
from ..conf.discovery import Discover
from ..conf.json_backend import SettingsBackendJson
from ..conf.yaml_backend import SettingsBackendYaml
from ..exceptions import BoussoleBaseException
from ..finder import ScssFinder
from ..project import ProjectBase


@click.command(
    "watch",
    short_help="Compile Sass project sources to CSS."
)
@click.option(
    "--backend",
    metavar="STRING",
    type=click.Choice(["json", "yaml"]),
    help="Settings format name",
    default="json"
)
@click.option(
    "--config",
    default=None,
    metavar="PATH",
    help="Path to a Boussole config file",
    type=click.Path(exists=True)
)
@click.pass_context
def compile_command(context, backend, config):
    """
    Compile Sass project sources to CSS
    """
    logger = logging.getLogger("boussole")
    logger.info("Building project")

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
        logger.critical(str(e))
        raise click.Abort()

    logger.debug("Settings file: {} ({})".format(
        config_filepath, config_engine._kind_name
    ))
    logger.debug("Project sources directory: {}".format(settings.SOURCES_PATH))
    logger.debug("Project destination directory: {}".format(settings.TARGET_PATH))
    logger.debug("Exclude patterns: {}".format(settings.EXCLUDES))
    if settings.HASH_SUFFIX:
        logger.debug("Build hash: {}".format(settings.HASH_SUFFIX))

    # Find all sources with their destination path
    try:
        compilable_files = ScssFinder().mirror_sources(
            settings.SOURCES_PATH,
            targetdir=settings.TARGET_PATH,
            excludes=settings.EXCLUDES,
            hashid=settings.HASH_SUFFIX,
        )
    except BoussoleBaseException as e:
        logger.error(str(e))
        raise click.Abort()

    # Build all compilable stylesheets
    compiler = SassCompileHelper()
    errors = 0
    for src, dst in compilable_files:
        logger.debug("Compile: {}".format(src))

        output_opts = {}
        success, message = compiler.safe_compile(settings, src, dst)

        if success:
            logger.info("Output: {}".format(message), **output_opts)
        else:
            errors += 1
            logger.error(message)

    # Ensure correct exit code if error has occured
    if errors:
        raise click.Abort()
