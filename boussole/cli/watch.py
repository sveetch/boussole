# -*- coding: utf-8 -*-
import time
import os
import click

from watchdog.observers import Observer

from boussole.conf.json_backend import SettingsBackendJson
from boussole.exceptions import SettingsBackendError
from boussole.watcher import SassWatchEventHandler


@click.command()
@click.option('--config', default=None, metavar='PATH',
              help='Path to a Boussole config file',
              type=click.Path(exists=True))
@click.pass_context
def watch_command(context, config):
    """
    Watch for change on your project Sass stylesheets then compile them to CSS.
    """
    logger = context.obj['logger']
    click.secho("Watching project", fg="green")

    # Load settings file
    try:
        backend = SettingsBackendJson(basedir=os.getcwd())
        settings = backend.load(filepath=config)
    except SettingsBackendError as e:
        logger.error(e.message)
        raise click.Abort()

    logger.info("Project sources directory: {}".format(
                settings.SOURCES_PATH))
    logger.info("Project destination directory: {}".format(
                settings.TARGET_PATH))
    logger.info("Exclude patterns: {}".format(
                settings.EXCLUDES))

    # Watcher settings
    watcher_templates_patterns = {
        'patterns': ['*.scss'],
        'ignore_patterns': ['*.part'],
        'ignore_directories': False,
        'case_sensitive': False,
    }

    # Registering event handler to observer
    observer = Observer()
    handler = SassWatchEventHandler(settings, logger,
                                    **watcher_templates_patterns)
    observer.schedule(handler, settings.SOURCES_PATH, recursive=True)

    # Start watching
    click.secho("Launching the watcher, use CTRL+C to stop it",
                fg="yellow")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        click.secho("CTRL+C used, stopping..", fg="yellow")
        observer.stop()

    observer.join()
