# -*- coding: utf-8 -*-
"""
Source watcher
==============

Watcher is almost *isolated* from command line code because it runs in an
infinite loop, so note that handlers directly output some informations with
``click.echo`` or ``logging.logger``.

"""
import os
import click

from pathtools.patterns import match_path
from watchdog.events import PatternMatchingEventHandler

from boussole.finder import ScssFinder
from boussole.compiler import SassCompileHelper


class SassWatchBaseEventHandler(PatternMatchingEventHandler):
    """
    Watchdog base handler for SASS sources

    The base handler does not compile the source which triggered an event,
    only its dependencies. This is common for libraries that are not intended
    to be recompiled.

    Args:
        settings (boussole.conf.model.Settings): Project settings.
        logger (logging.Logger): Logger object to write messages.
        inspector (boussole.inspector.ScssInspector): Inspector instance.

    Attributes:
        settings (boussole.conf.model.Settings): Filled from argument.
        logger (logging.Logger): Filled from argument.
        inspector (boussole.inspector.ScssInspector): Filled from argument.
        finder (boussole.finder.ScssFinder): Finder instance.
        compiler (boussole.compiler.SassCompileHelper): Sass compile helper
            object.
        compilable_files (dict): Pair of (source path, destination path) to
            compile. Automatically update from ``index()`` method.
        source_files (list): List of source path to compile. Automatically
            update from ``index()`` method.
    """
    def __init__(self, settings, logger, inspector, *args, **kwargs):
        self.settings = settings
        self.logger = logger
        self.inspector = inspector

        self.finder = ScssFinder()
        self.compiler = SassCompileHelper()

        self.compilable_files = {}
        self.source_files = []

        super(SassWatchBaseEventHandler, self).__init__(*args, **kwargs)

    def index(self):
        """
        Reset inspector buffers and index project sources dependencies.

        This have to be executed each time an event occurs.
        """
        compilable_files = self.finder.mirror_sources(
            self.settings.SOURCES_PATH,
            targetdir=self.settings.TARGET_PATH,
            excludes=self.settings.EXCLUDES
        )
        self.compilable_files = dict(compilable_files)
        self.source_files = self.compilable_files.keys()

        # Init inspector and do first inspect
        self.inspector.reset()
        self.inspector.inspect(*self.source_files,
                               library_paths=self.settings.LIBRARY_PATHS)

    def compile_source(self, sourcepath):
        """
        Compile source to its destination

        Check if the source is eligible to compile (not partial and allowed
        from exclude patterns)

        Args:
            sourcepath (string): Sass source path to compile to its
                destination using project settings.

        Returns:
            tuple or None: A pair of (sourcepath, destination), if source has
                been compiled (or at least tried). If the source was not
                eligible to compile, return will be ``None``.
        """
        relpath = os.path.relpath(sourcepath, self.settings.SOURCES_PATH)

        conditions = {
            'sourcedir': None,
            'nopartial': True,
            'exclude_patterns': self.settings.EXCLUDES,
            'excluded_libdirs': self.settings.LIBRARY_PATHS,
        }
        if self.finder.match_conditions(sourcepath, **conditions):
            destination = self.finder.get_destination(
                relpath,
                targetdir=self.settings.TARGET_PATH
            )

            self.logger.debug("* Compile: {}".format(sourcepath))
            output_opts = {}
            success, message = self.compiler.safe_compile(self.settings, sourcepath, destination)

            if success:
                click.secho("* Compiled: {}".format(message), **output_opts)
            else:
                click.secho(message, fg='red')

            return sourcepath, destination

        return None

    def compile_dependencies(self, sourcepath):
        """
        Apply compile on all dependencies

        Args:
            sourcepath (string): Sass source path to compile to its
                destination using project settings.
        """
        parents = self.inspector.parents(sourcepath)

        return filter(None, [self.compile_source(item) for item in parents])

    def on_any_event(self, event):
        """
        Catch-all event handler (moved, created, deleted, changed).

        Before any event, index project to have the right and current
        dependencies map.

        Args:
            event: Watchdog event ``watchdog.events.FileSystemEvent``.
        """
        self.index()

    def on_moved(self, event):
        """
        Called when a file or a directory is moved or renamed.

        Many editors don't directly change a file, instead they make a
        transitional file like ``*.part`` then move it to the final filename.

        Args:
            event: Watchdog event, either ``watchdog.events.DirMovedEvent`` or
                ``watchdog.events.FileModifiedEvent``.
        """
        # We are only interested for final file, not transitional file
        # from editors (like *.part)
        pathtools_options = {
            'included_patterns': self.patterns,
            'excluded_patterns': self.ignore_patterns,
            'case_sensitive': self.case_sensitive,
        }
        if match_path(event.dest_path, **pathtools_options):
            self.logger.info("Change detected from a move on: %s",
                              event.dest_path)
            self.compile_dependencies(event.dest_path)
            click.secho("")

    def on_created(self, event):
        """
        Called when a new file or directory is created.

        Todo:
            This should be also used (extended from another class?) to watch
            for some special name file (like ".boussole-watcher-stop" create to
            raise a KeyboardInterrupt, so we may be able to unittest the
            watcher (click.CliRunner is not able to send signal like CTRL+C
            that is required to watchdog observer loop)

        Args:
            event: Watchdog event, either ``watchdog.events.DirCreatedEvent``
                or ``watchdog.events.FileCreatedEvent``.
        """
        self.logger.info("Change detected from a create on: %s",
                          event.src_path)

        self.compile_dependencies(event.src_path)
        click.secho("")


    def on_modified(self, event):
        """
        Called when a file or directory is modified.

        Args:
            event: Watchdog event, ``watchdog.events.DirModifiedEvent`` or
                ``watchdog.events.FileModifiedEvent``.
        """
        self.logger.info("Change detected from an edit on: %s",
                          event.src_path)

        self.compile_dependencies(event.src_path)
        click.secho("")


    def on_deleted(self, event):
        """
        Called when a file or directory is deleted.

        Todo:
            Bugged with inspector and sass compiler since the does not exists
            anymore.

        Args:
            event: Watchdog event, ``watchdog.events.DirDeletedEvent`` or
                ``watchdog.events.FileDeletedEvent``.
        """
        self.logger.info("Change detected from deletion of: %s",
                          event.src_path)

        self.compile_dependencies(event.src_path)
        click.secho("")


class SassWatchSourcesEventHandler(SassWatchBaseEventHandler):
    """
    Watchdog handler where the source that trigger event is compiled (if
    eligible) with its dependencies.
    """
    def compile_dependencies(self, sourcepath):
        """
        Apply compile on all dependencies and the source itself.

        Args:
            sourcepath (string): Sass source path to compile to its
                destination using project settings.
        """
        parents = self.inspector.parents(sourcepath)

        # Also add the current event related path
        parents.add(sourcepath)

        return filter(None, [self.compile_source(item) for item in parents])
