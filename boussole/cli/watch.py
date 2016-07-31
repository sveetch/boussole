# -*- coding: utf-8 -*-
import time
import os
import click

import six

from watchdog.observers import Observer

from boussole.conf.json_backend import SettingsBackendJson
from boussole.exceptions import SettingsBackendError
from boussole.inspector import ScssInspector
from boussole.watcher import (WatchdogLibraryEventHandler,
                              WatchdogProjectEventHandler)


@click.command('watch', short_help='Watch for change on your SASS project.')
@click.option('--config', default=None, metavar='PATH',
              help='Path to a Boussole config file',
              type=click.Path(exists=True))
@click.pass_context
def watch_command(context, config):
    """
    Watch for change on your SASS project sources then compile them to CSS.

    Watched events are:

    \b
    * Create: when a new source file is created;
    * Change: when a source is changed;
    * Delete: when a source is deleted;
    * Move: When a source file is moved;

    Almost all errors occurring during compile won't break watcher, so you can
    resolve them and watcher will try again to compile once an a new event
    occurs.

    You can stop watcher using key combo "CTRL+C" (or CMD+C on MacOSX).
    """
    logger = context.obj['logger']
    logger.info("Watching project")

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
    logger.warning(u"Launching the watcher, use CTRL+C to stop it")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.warning(u"CTRL+C used, stopping..")
        observer.stop()

    observer.join()
