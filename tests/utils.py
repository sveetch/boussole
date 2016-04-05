# -*- coding: utf-8 -*-
"""
Some utilities and common stuff for tests
"""
import os

from boussole.conf.model import Settings
from boussole.inspector import ScssInspector
from boussole.watcher import SassLibraryEventHandler, SassProjectEventHandler
from boussole.logs import init_logger

class DummyBaseEvent(object):
    """
    Dummy event to pass to almost all handler event methods
    """
    def __init__(self, filepath):
        self.src_path = filepath


class DummyMoveEvent(object):
    """
    Dummy event to pass to handler event 'move' method
    """
    def __init__(self, filepath):
        self.dest_path = filepath


class DummyBaseHandler(object):
    """
    Fake watchdog event handler

    Reproduce some behavior from watchdog event handler to ease tests
    """
    def __init__(self, *args, **kwargs):
        self.patterns = kwargs.pop('patterns')
        self.ignore_patterns = kwargs.pop('ignore_patterns')
        self.ignore_directories = kwargs.pop('ignore_directories')
        self.case_sensitive = kwargs.pop('case_sensitive')
        super(DummyBaseHandler, self).__init__(*args, **kwargs)

    def on_moved(self, event):
        self.on_any_event(event)
        super(DummyBaseHandler, self).on_moved(event)

    def on_created(self, event):
        self.on_any_event(event)
        super(DummyBaseHandler, self).on_created(event)

    def on_modified(self, event):
        self.on_any_event(event)
        super(DummyBaseHandler, self).on_modified(event)

    def on_deleted(self, event):
        self.on_any_event(event)
        super(DummyBaseHandler, self).on_deleted(event)


class UnitTestableLibraryEventHandler(DummyBaseHandler, SassLibraryEventHandler):
    """
    Testable watch event handler for library sources
    """
    pass


class UnitTestableProjectEventHandler(DummyBaseHandler, SassProjectEventHandler):
    """
    Testable watch event handler for project sources
    """
    pass


def join_basedir(basedir):
    """
    Shortcut to join basedir to given path
    """
    def proceed_joining(path):
        return os.path.join(basedir, path)
    return proceed_joining


def start_env(basedir):
    """
    Init all needed stuff for handler testing
    """
    join_basedir_curry = join_basedir(basedir.strpath)

    logger = init_logger('DEBUG', printout=False)

    inspector = ScssInspector()

    minimal_conf = {
        'SOURCES_PATH': basedir.join('sass').strpath,
        'TARGET_PATH': basedir.join('css').strpath,
        'LIBRARY_PATHS': [basedir.join('lib').strpath],
    }
    settings = Settings(initial=minimal_conf)

    watcher_opts = {
        'patterns': ['*.scss'],
        'ignore_patterns': ['*.part'],
        'ignore_directories': False,
        'case_sensitive': True,
    }
    return join_basedir_curry, logger, inspector, settings, watcher_opts


def build_sample_structure(settings_object, basedir):
    """
    Build sample files structure for handler testing
    """
    # Write needed dirs
    os.makedirs(settings_object.SOURCES_PATH)
    os.makedirs(settings_object.TARGET_PATH)
    os.makedirs(os.path.join(settings_object.LIBRARY_PATHS[0], "components"))

    # Write a minimal main SASS source importing partial
    source = "\n".join((
        """/* Main sample */""",
        """@import "toinclude";""",
        """#content{ color: red; }""",
    ))
    with open(basedir.join('sass/main.scss').strpath, 'w') as f:
        f.write(source)

    # Write a main SASS source importing minimal source
    source = "\n".join((
        """/* Main importing sample */""",
        """@import "main";""",
    ))
    with open(basedir.join('sass/main_importing.scss').strpath, 'w') as f:
        f.write(source)

    # Write a main SASS source importing library component and partial source
    source = "\n".join((
        """/* Main importing library */""",
        """@import "toinclude";""",
        """@import "components/buttons";""",
    ))
    with open(basedir.join('sass/main_usinglib.scss').strpath, 'w') as f:
        f.write(source)

    # Write a partial SASS source to include
    source = "\n".join((
        """/* Partial source to include */""",
        """.included-partial{ color: gold !important; }""",
    ))
    with open(basedir.join('sass/_toinclude.scss').strpath, 'w') as f:
        f.write(source)

    # Write a partial SASS source to ignore
    source = "\n".join((
        """/* Partial source to ignore because not included */""",
        """.toignore-partial{ font-weight: bold; }""",
    ))
    with open(basedir.join('sass/_notincluded.scss').strpath, 'w') as f:
        f.write(source)

    # Write a main source within library directory
    source = "\n".join((
        """/* Main source for library */""",
        """@import "components/buttons";""",
    ))
    with open(basedir.join('lib/libmain.scss').strpath, 'w') as f:
        f.write(source)

    # Write a partial source within library directory
    source = "\n".join((
        """/* Buttons component */""",
        """.button{ display: block; border: 1px solid black; padding: 5px; }""",
    ))
    with open(basedir.join('lib/components/_buttons.scss').strpath, 'w') as f:
        f.write(source)
