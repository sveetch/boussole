# -*- coding: utf-8 -*-
"""
Source watcher
==============

Watcher is almost *isolated* from command line code because it runs in an
infinite loop, so note that handlers directly output some informations on a
``logging.logger``.

"""
import os
import logging

import six

from pathtools.patterns import match_path
from watchdog.events import PatternMatchingEventHandler

from boussole.exceptions import BoussoleBaseException
from boussole.finder import ScssFinder
from boussole.compiler import SassCompileHelper


class SassLibraryEventHandler(object):
    """
    Watch mixin handler for library sources

    Handler does not compile source which triggered an event,
    only its parent dependencies. Because libraries are not intended to be
    compiled.

    Args:
        settings (boussole.conf.model.Settings): Project settings.
        inspector (boussole.inspector.ScssInspector): Inspector instance.

    Attributes:
        settings (boussole.conf.model.Settings): Filled from argument.
        logger (logging.Logger): Boussole logger.
        inspector (boussole.inspector.ScssInspector): Filled from argument.
        finder (boussole.finder.ScssFinder): Finder instance.
        compiler (boussole.compiler.SassCompileHelper): Sass compile helper
            object.
        compilable_files (dict): Pair of (source path, destination path) to
            compile. Automatically update from ``index()`` method.
        source_files (list): List of source path to compile. Automatically
            update from ``index()`` method.
        _event_error (bool): Internal flag setted to ``True`` if error has
            occured within an event. ``index()`` will reboot it to ``False``
            each time a new event occurs.
    """
    SUPPORTED_EVENTS = (
        "moved",
        "created",
        "modified",
        "deleted",
    )

    def __init__(self, settings, inspector, *args, **kwargs):
        self.settings = settings
        self.inspector = inspector

        self.logger = logging.getLogger("boussole")
        self.finder = ScssFinder()
        self.compiler = SassCompileHelper()

        self.compilable_files = {}
        self.source_files = []
        self._event_error = False

        super(SassLibraryEventHandler, self).__init__(*args, **kwargs)

    def is_valid_event(self, event):
        """
        Check if given event is valid event for index method.

        An event is considered valid if event type is supported (from
        ``SassLibraryEventHandler.SUPPORTED_EVENTS``) and file is allowed (from
        method ``ImportPathsResolver.is_allowed_source``).

        Args:
            event (watchdog.events.FileSystemEvent): Watchdog file system event.

        Returns:
            bool: True if valid, else False.
        """
        # Don't continue for non supported event
        if event.event_type not in self.SUPPORTED_EVENTS or event.is_directory:
            return False

        # We commonly care only about destination path, but it is missing from
        # some event where the source path is the only one available and so the
        # legit path to look at
        target_path = event.src_path
        if hasattr(event, "dest_path"):
            target_path = event.dest_path

        # Don't continue for files we don't care about
        if not self.inspector.is_allowed_source(target_path):
            return False

        return True

    def index(self, event):
        """
        Reset inspector buffers and index project sources dependencies.

        This have to be executed each time an event occurs.

        Args:
            event (watchdog.events.FileSystemEvent): Watchdog file system event.

        Returns:
            bool: True if allowed, else False.

        Note:
            If a Boussole exception occurs during operation, it will be catched
            and an error flag will be set to ``True`` so event operation will
            be stopped without blocking or breaking watchdog observer.
        """
        self._event_error = False

        # Don't continue for non valid event
        if not self.is_valid_event(event):
            return

        try:
            compilable_files = self.finder.mirror_sources(
                self.settings.SOURCES_PATH,
                targetdir=self.settings.TARGET_PATH,
                excludes=self.settings.EXCLUDES
            )
            self.compilable_files = dict(compilable_files)
            self.source_files = self.compilable_files.keys()

            # Init inspector and do first inspect
            self.inspector.reset()
            self.inspector.inspect(
                *self.source_files,
                library_paths=self.settings.LIBRARY_PATHS
            )
        except BoussoleBaseException as e:
            self._event_error = True
            self.logger.error(six.text_type(e))

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

            self.logger.debug(u"Compile: {}".format(sourcepath))
            success, message = self.compiler.safe_compile(
                self.settings,
                sourcepath,
                destination
            )

            if success:
                self.logger.info(u"Output: {}".format(message))
            else:
                self.logger.error(message)

            return sourcepath, destination

        return None

    def compile_dependencies(self, sourcepath, include_self=False):
        """
        Register source(s) for compile and possibly its dependencies.

        Args:
            sourcepath (string): Sass source path to compile to its
                destination using project settings.

        Keyword Arguments:
            include_self (bool): If ``True`` the given sourcepath is added to
                items to compile, else only its dependencies are compiled.
        """
        items = self.inspector.parents(sourcepath)

        # Also add the current event related path
        if include_self:
            items.add(sourcepath)

        return filter(None, [self.compile_source(item) for item in items])

    def on_any_event(self, event):
        """
        Catch-all event handler (moved, created, deleted, changed).

        Before any event, we index project to have the right and current
        dependencies map.

        Args:
            event: Watchdog event ``watchdog.events.FileSystemEvent``.
        """
        self.index(event)

    def on_moved(self, event):
        """
        Called when a file or a directory is moved or renamed.

        Many editors don't directly change a file, instead they make a
        transitional file like ``*.part`` then move it to the final filename.

        Args:
            event: Watchdog event, either ``watchdog.events.DirMovedEvent`` or
                ``watchdog.events.FileModifiedEvent``.
        """
        if not self._event_error:
            # We are only interested for final file, not transitional file
            # from editors (like *.part)
            pathtools_options = {
                'included_patterns': self.patterns,
                'excluded_patterns': self.ignore_patterns,
                'case_sensitive': self.case_sensitive,
            }
            # Apply pathtool matching on destination since Watchdog only
            # automatically apply it on source
            if match_path(event.dest_path, **pathtools_options):
                self.logger.info(u"Change detected from a move on: %s",
                                 event.dest_path)
                self.compile_dependencies(event.dest_path)

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
        if not self._event_error:
            self.logger.info(u"Change detected from a create on: %s",
                             event.src_path)

            self.compile_dependencies(event.src_path)

    def on_modified(self, event):
        """
        Called when a file or directory is modified.

        Args:
            event: Watchdog event, ``watchdog.events.DirModifiedEvent`` or
                ``watchdog.events.FileModifiedEvent``.
        """
        if not self._event_error:
            self.logger.info(u"Change detected from an edit on: %s",
                             event.src_path)

            self.compile_dependencies(event.src_path)

    def on_deleted(self, event):
        """
        Called when a file or directory is deleted.

        Args:
            event: Watchdog event, ``watchdog.events.DirDeletedEvent`` or
                ``watchdog.events.FileDeletedEvent``.
        """
        if not self._event_error:
            self.logger.info(u"Change detected from deletion of: %s",
                             event.src_path)
            # Never try to compile the deleted source
            self.compile_dependencies(event.src_path, include_self=False)


class SassProjectEventHandler(SassLibraryEventHandler):
    """
    Watch mixin handler for project sources.

    Warning:
        DO NOT use this handler to watch libraries, there is a risk the
        compiler will try to compile their sources in a wrong directory.

    Source that trigger event is compiled (if eligible) with its dependencies.
    """
    def compile_dependencies(self, sourcepath, include_self=True):
        """
        Same as inherit method but the default value for keyword argument
        ``ìnclude_self`` is ``True``.
        """
        return super(SassProjectEventHandler, self).compile_dependencies(
            sourcepath,
            include_self=include_self
        )


class WatchdogLibraryEventHandler(SassLibraryEventHandler,
                                  PatternMatchingEventHandler):
    """
    Watchdog event handler for library sources
    """
    pass


class WatchdogProjectEventHandler(SassProjectEventHandler,
                                  PatternMatchingEventHandler):
    """
    Watchdog event handler for project sources.

    Warning:
        DO NOT use this handler to watch libraries, there is a risk the
        compiler will try to compile their sources in a wrong directory.
    """
    pass
