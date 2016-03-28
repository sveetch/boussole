# -*- coding: utf-8 -*-
"""
Source watcher
==============

"""
import os

from pathtools.patterns import match_path
from watchdog.events import PatternMatchingEventHandler

from boussole.finder import ScssFinder
from boussole.inspector import ScssInspector


class SassWatchEventHandler(PatternMatchingEventHandler):
    """
    Watchdog handler for SASS sources

    Args:
        settings (boussole.conf.model.Settings): Project settings.
        logger (logging.Logger): Logger object to write messages.

    Attributes:
        settings (boussole.conf.model.Settings): Filled from argument.
        logger (logging.Logger): Filled from argument.
        inspector (boussole.inspector.ScssInspector): Inspector instance.
        finder (boussole.finder.ScssFinder): Finder instance.
        compilable_files (dict): Pair of (source path, destination path) to
            compile. Automatically update from ``reset()`` method.
        source_files (list): List of source path to compile. Automatically
            update from ``reset()`` method.
    """
    def __init__(self, settings, logger, *args, **kwargs):
        self.settings = settings
        self.logger = logger

        self.inspector = ScssInspector()
        self.finder = ScssFinder()

        self.compilable_files = {}
        self.source_files = []

        self.reset()

        super(SassWatchEventHandler, self).__init__(*args, **kwargs)

    def reset(self):
        """
        Reset inspector and inspect again project sources.

        This should be executed each time a change occurs after compiling the
        sources.
        """
        compilable_files = self.finder.mirror_sources(
            self.settings.SOURCES_PATH,
            targetdir=self.settings.TARGET_PATH,
            excludes=self.settings.EXCLUDES
        )
        self.compilable_files = dict(compilable_files)
        self.source_files = self.compilable_files.keys()

        self.logger.debug(self.source_files)

        # Init inspector and do first inspect
        self.inspector.reset()
        self.inspector.inspect(*self.source_files,
                               library_paths=self.settings.LIBRARY_PATHS)

    def on_moved(self, event):
        """
        Called when a file or a directory is moved or renamed.

        Args:
            event: Watchdog event, either ``watchdog.events.DirMovedEvent`` or
                ``watchdog.events.FileModifiedEvent``.
        """
        # We are only interested for the destination, not transitionnal file
        # from editor (like *.part)
        if match_path(event.dest_path,
                      included_patterns=self.patterns,
                      excluded_patterns=self.ignore_patterns,
                      case_sensitive=self.case_sensitive):
            self.logger.debug("Change detected from a move on: %s",
                              event.dest_path)

            parents = self.inspector.parents(event.dest_path)
            for item in parents:
                relative_filepath = os.path.relpath(item,
                                                    self.settings.SOURCES_PATH)

                # Bother only about not partial and allowed (from exclude
                # patterns) files
                if not self.finder.is_partial(relative_filepath) and \
                   self.finder.is_allowed(
                       relative_filepath,
                       excludes=self.settings.EXCLUDES):
                    print "Pretending to compile:", relative_filepath
                    # self.build_for_item(event.dest_path)

    def on_created(self, event):
        """
        Called when a file or directory is created.

        Args:
            event: Watchdog event, either ``watchdog.events.DirCreatedEvent``
                or ``watchdog.events.FileCreatedEvent``.
        """
        self.logger.debug("Change detected from a create on: %s",
                          event.src_path)
        # self.build_for_item(event.src_path)

    def on_modified(self, event):
        """
        Called when a file or directory is modified.

        Args:
            event: Watchdog event, ``watchdog.events.DirModifiedEvent`` or
                ``watchdog.events.FileModifiedEvent``.
        """
        self.logger.debug("Change detected from an edit on: %s",
                          event.src_path)
        # self.build_for_item(event.src_path)

    def build_for_item(self, path):
        """
        Todo: Compile all sources related
        """
        pass
