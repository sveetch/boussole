# -*- coding: utf-8 -*-
"""
Source watcher
==============

"""
import os
import json

from pathtools.patterns import match_path
from watchdog.events import PatternMatchingEventHandler

from boussole.finder import ScssFinder
from boussole.inspector import ScssInspector

class SassWatchEventHandler(PatternMatchingEventHandler):
    """
    Watchdog handler for SASS sources
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
        Reset inspector and inspect again project sources

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
        self.inspector.inspect(*self.source_files, library_paths=self.settings.LIBRARY_PATHS)

    def on_moved(self, event):
        # We are only interested for the destination, not transitionnal file
        # from editor (like *.part)
        if match_path(event.dest_path,
                included_patterns=self.patterns,
                excluded_patterns=self.ignore_patterns,
                case_sensitive=self.case_sensitive):
            self.logger.debug("Change detected from a move on: %s", event.dest_path)

            parents = self.inspector.parents(event.dest_path)
            for item in parents:
                relative_filepath = os.path.relpath(item, self.settings.SOURCES_PATH)

                # Bother only about not partial and allowed (from exclude
                # patterns) files
                if not self.finder.is_partial(relative_filepath) and \
                   self.finder.is_allowed(relative_filepath, excludes=self.settings.EXCLUDES):
                    print "Pretending to compile:", relative_filepath
                    #self.build_for_item(event.dest_path)

    def on_created(self, event):
        self.logger.debug("Change detected from a create on: %s", event.src_path)
        #self.build_for_item(event.src_path)

    def on_modified(self, event):
        self.logger.debug("Change detected from an edit on: %s", event.src_path)
        #self.build_for_item(event.src_path)

    def build_for_item(self, path):
        """
        (Re)build all pages using the changed template

        ``path`` argument is a template path
        """
        rel_path = self.get_relative_path(path)

        # Search in the registry if the file is a knowed template dependancy
        if rel_path in self.pages_env.registry.elements:
            self.logger.debug("Build required for: %s", rel_path)

            requires = self.pages_env.registry.get_pages_from_dependency(rel_path)
            self.logger.debug("Requires for rebuild: %s", requires)
            self.pages_env.build_bulk(requires)
