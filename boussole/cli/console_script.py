"""
Main entrance to commandline actions
"""
import click

from boussole.cli.version import version_command
from boussole.cli.compile import compile_command
from boussole.cli.watch import watch_command


def main():
    print "Hello World!"


@click.group()
@click.option('--config', default=None, metavar='PATH',
              help='Path to a Boussole config file')
@click.pass_context
def cli_frontend(ctx, config):
    """
    Boussole is a commandline interface to build SASS projects using libsass.
    """
    # Init the default context that will be passed to commands
    # Not really used since settings is imported from its module
    ctx.obj = {}

    ## Override config directory from given option if any
    #if config_dir:
        #settings.set_setting('CONFIG_DIR', config_dir)


# Attach commands methods to the main grouper
cli_frontend.add_command(version_command, name="version")
cli_frontend.add_command(compile_command, name="compile")
cli_frontend.add_command(watch_command, name="watch")
