# -*- coding: utf-8 -*-
import time
import os
import click
import logging

from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver

from ..conf.discovery import Discover
from ..conf.json_backend import SettingsBackendJson
from ..conf.yaml_backend import SettingsBackendYaml
from ..exceptions import BoussoleBaseException
from ..inspector import ScssInspector
from ..project import ProjectBase
from ..watcher import WatchdogLibraryEventHandler, WatchdogProjectEventHandler


@click.command(
    "watch",
    short_help="Watch for change on your Sass project."
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
@click.option(
    "--poll",
    is_flag=True,
    help="Use Watchdog polling observer"
)
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

    Almost all errors occurring during compile won"t break watcher, so you can
    resolve them and watcher will try again to compile once a new event
    occurs.

    You can stop watcher using key combo "CTRL+C" (or CMD+C on MacOSX).
    """
    logger = logging.getLogger("boussole")
    logger.info("Watching project")

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

    # Watcher settings
    watcher_templates_patterns = {
        "patterns": ["*.scss", "*.sass"],
        "ignore_patterns": ["*.part"],
        "ignore_directories": False,
        "case_sensitive": True,
    }

    # Init inspector instance shared through all handlers
    inspector = ScssInspector()

    if not poll:
        logger.debug("Using Watchdog native platform observer")
        observer = Observer()
    else:
        logger.debug("Using Watchdog polling observer")
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
    logger.warning("Launching the watcher, use CTRL+C to stop it")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.warning("CTRL+C used, stopping..")
        observer.stop()

    observer.join()
