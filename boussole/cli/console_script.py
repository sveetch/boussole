"""
Main entrance to commandline actions
"""
import click

from boussole.cli.version import version_command
from boussole.cli.compile import compile_command
from boussole.cli.watch import watch_command
from boussole.logs import BOUSSOLE_LOGGER_CONF, init_logger


# Help alias on '-h' argument
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('-v', '--verbose', count=True)
@click.pass_context
def cli_frontend(ctx, verbose):
    """
    Boussole is a commandline interface to build SASS projects using libsass.

    Every project will need a config file containing all needed settings to
    build it.
    """
    # Limit verbosity from enabled levels
    if verbose > len(BOUSSOLE_LOGGER_CONF)-1:
        verbose = len(BOUSSOLE_LOGGER_CONF)-1
    # Verbosity is the inverse of logging levels
    levels = [item[0] for item in BOUSSOLE_LOGGER_CONF]
    levels.reverse()
    # Init the logger config
    root_logger = init_logger(levels[verbose])

    root_logger.info("Logging level fixed to '{}'".format(levels[verbose]))

    # Init the default context that will be passed to commands
    ctx.obj = {
        'verbosity': verbose,
        'logger': root_logger,
    }


# Attach commands methods to the main grouper
cli_frontend.add_command(version_command, name="version")
cli_frontend.add_command(compile_command, name="compile")
cli_frontend.add_command(watch_command, name="watch")
