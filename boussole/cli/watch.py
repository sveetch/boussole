# -*- coding: utf-8 -*-
import time
import os
import click
import logging

import six

from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver

from boussole.exceptions import SettingsBackendError
from boussole.inspector import ScssInspector
from boussole.watcher import (WatchdogLibraryEventHandler,
                              WatchdogProjectEventHandler)
from boussole.project import ProjectBase


@click.command('watch', short_help='Watch for change on your Sass project.')
@click.option('--backend', metavar='STRING',
              type=click.Choice(['json', 'yaml']),
              help="Settings format name",
              default="json")
@click.option('--config', default=None, metavar='PATH',
              help='Path to a Boussole config file',
              type=click.Path(exists=True))
@click.option('--poll', is_flag=True, help='Use Watchdog polling observer')
@click.pass_context
def watch_command(context, backend, config, poll):
    """
    Watch for change on your Sass project sources then compile them to CSS.

    Watched events are:

    \b
    * Create: when a new source file is created;
    * Change: when a source is changed;
    * Delete: when a source is deleted;
    * Move: When a source file is moved in watched dirs. Also occurs with
      editor transition file;

    Almost all errors occurring during compile won't break watcher, so you can
    resolve them and watcher will try again to compile once a new event
    occurs.

    You can stop watcher using key combo "CTRL+C" (or CMD+C on MacOSX).
    """
    logger = logging.getLogger("boussole")
    logger.info("Watching project")

    # Load settings file
    try:
        project = ProjectBase(backend_name=backend, basedir=os.getcwd())

        # If not given, config file name is setted from backend default
        # filename
        if not config:
            config = project.backend_engine._default_filename

        settings = project.backend_engine.load(filepath=config)
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

    if not poll:
        logger.debug(u"Using Watchdog native platform observer")
        observer = Observer()
    else:
        logger.debug(u"Using Watchdog polling observer")
        observer = PollingObserver()

    # Init event handlers
    project_handler = WatchdogProjectEventHandler(settings, inspector,
                                                  **watcher_templates_patterns)

    lib_handler = WatchdogLibraryEventHandler(settings, inspector,
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
