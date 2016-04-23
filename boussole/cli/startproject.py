# -*- coding: utf-8 -*-
import os
import click

from boussole.exceptions import SettingsInvalidError
from boussole.project import ProjectStarter


@click.command('startproject', short_help="Create a new SASS project.")
@click.option('--basedir', metavar='PATH',
              prompt="Project base directory",
              help=("Base directory where settings filename and project "
                    "structure will be created."),
              default=".")
@click.option('--config', metavar='PATH',
              prompt="Settings file name",
              help="Settings file name",
              default="settings.json")
@click.option('--sourcedir', metavar='PATH',
              prompt="Sources directory",
              help="Directory (within base dir) for your SASS sources.",
              default="scss")
@click.option('--targetdir', metavar='PATH',
              prompt="Target directory",
              help="Directory (within base dir) where to write compiled "
                   "files.",
              default="css")
@click.pass_context
def startproject_command(context, basedir, config, sourcedir, targetdir):
    """
    Create a new SASS project

    This will prompt you to define your project configuration in a settings
    file then create needed directory structure.

    Arguments "basedir", "config", "sourcedir", "targetdir" can not be empty.
    """
    logger = context.obj['logger']

    try:
        results = ProjectStarter().init(*(
            basedir,
            config,
            sourcedir,
            targetdir,
        ), cwd=os.getcwd())
    except SettingsInvalidError as e:
        logger.critical(e.message)
        raise click.Abort()
    else:
        logger.info("Project directory structure and configuration file have "
                    "been created.")

        logger.info("Now you should start to create some SASS sources into "
                    "'{}', then compile them "
                    "using:".format(results['sourcedir']))

        logger.info("    boussole compile "
                    "--config={}".format(results['config']))
