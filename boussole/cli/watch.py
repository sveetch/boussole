# -*- coding: utf-8 -*-
import time
import os
import click

from watchdog.observers import Observer

from boussole.conf.json_backend import SettingsBackendJson
from boussole.exceptions import SettingsBackendError
from boussole.inspector import ScssInspector
from boussole.watcher import (WatchdogLibraryEventHandler,
                              WatchdogProjectEventHandler)


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
    logger.info("Watching project")

    # Load settings file
    try:
        backend = SettingsBackendJson(basedir=os.getcwd())
        settings = backend.load(filepath=config)
    except SettingsBackendError as e:
        logger.error(e.message)
        raise click.Abort()

    logger.debug("* Project sources directory: {}".format(
                settings.SOURCES_PATH))
    logger.debug("* Project destination directory: {}".format(
                settings.TARGET_PATH))
    logger.debug("* Exclude patterns: {}".format(
                settings.EXCLUDES))

    # Watcher settings
    watcher_templates_patterns = {
        'patterns': ['*.scss'],
        'ignore_patterns': ['*.part'],
        'ignore_directories': False,
        'case_sensitive': True,
    }

    # Init inspector instance shared through all handlers
    inspector = ScssInspector()

    # Registering event handlers to observer
    observer = Observer()
    project_handler = WatchdogProjectEventHandler(settings, logger, inspector,
                                                  **watcher_templates_patterns)

    lib_handler = WatchdogLibraryEventHandler(settings, logger, inspector,
                                              **watcher_templates_patterns)

    # Observe source directory
    observer.schedule(project_handler, settings.SOURCES_PATH, recursive=True)

    # Also observe libraries directories
    for libpath in settings.LIBRARY_PATHS:
        observer.schedule(lib_handler, libpath, recursive=True)

    # Start watching
    logger.warning("Launching the watcher, use CTRL+C to stop it")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.warning("CTRL+C used, stopping..")
        observer.stop()

    observer.join()
