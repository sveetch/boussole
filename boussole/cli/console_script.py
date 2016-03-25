"""
Main entrance to commandline actions
"""
# import os
import click

from boussole.cli.version import version_command
from boussole.cli.compile import compile_command
from boussole.cli.watch import watch_command

# from boussole.conf.json_backend import SettingsBackendJson


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
# @click.option('--config', default=None, metavar='PATH',
#              help='Path to a Boussole config file',
#              type=click.Path(exists=True))
@click.pass_context
def cli_frontend(ctx):
    """
    Boussole is a commandline interface to build SASS projects using libsass.

    Every project will need a config file containing all need settings to
    build it.

    If no config file is given from argument "--config", default behavior is
    to search for a "settings.json" in the current directory.
    """
    # Init the default context that will be passed to commands
    ctx.obj = {
        # 'cwd': os.getcwd(),
    }

    # backend = SettingsBackendJson(basedir=os.getcwd())
    # ctx.obj['settings'] = backend.load(filepath=config)


# Attach commands methods to the main grouper
cli_frontend.add_command(version_command, name="version")
cli_frontend.add_command(compile_command, name="compile")
cli_frontend.add_command(watch_command, name="watch")
