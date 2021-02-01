# -*- coding: utf-8 -*-
"""
Some utilities and common stuff for tests
"""
import os

from boussole.conf.model import Settings
from boussole.inspector import ScssInspector
from boussole.watcher import SassLibraryEventHandler, SassProjectEventHandler


class DummyBaseEvent(object):
    """
    Dummy event base to pass to almost all handler event methods
    """
    event_type = "boussole-dummy"
    is_directory = False

    def __init__(self, filepath):
        self.src_path = filepath
        self.dest_path = filepath


class DummyCreatedEvent(DummyBaseEvent):
    """
    Dummy event to pass to handler event 'on_created' method
    """
    event_type = "created"


class DummyModifiedEvent(DummyBaseEvent):
    """
    Dummy event to pass to handler event 'on_modified' method
    """
    event_type = "modified"


class DummyDeletedEvent(DummyBaseEvent):
    """
    Dummy event to pass to handler event 'on_deleted' method
    """
    event_type = "deleted"


class DummyMoveEvent(DummyBaseEvent):
    """
    Dummy event to pass to handler event 'on_moved' method
    """
    event_type = "moved"


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
    Return a shortcut function to join basedir to given path
    """
    def proceed_joining(path):
        return os.path.join(basedir, path)
    return proceed_joining


def start_env(basedir):
    """
    Initialize a basedir path, a dummy Settings object, Inspector object and
    Watcher options needed for handler testing.
    """
    join_basedir_curry = join_basedir(basedir.strpath)

    inspector = ScssInspector()

    minimal_conf = {
        'SOURCES_PATH': basedir.join('sass').strpath,
        'TARGET_PATH': basedir.join('css').strpath,
        'LIBRARY_PATHS': [basedir.join('lib').strpath],
    }
    settings = Settings(initial=minimal_conf)

    watcher_opts = {
        'patterns': ['*.scss', '*.sass'],
        'ignore_patterns': ['*.part'],
        'ignore_directories': False,
        'case_sensitive': True,
    }
    return join_basedir_curry, inspector, settings, watcher_opts


def build_scss_sample_structure(settings_object, basedir):
    """
    Build Scss sample files structure for handler testing
    """
    # Write needed dirs
    os.makedirs(settings_object.SOURCES_PATH)
    os.makedirs(settings_object.TARGET_PATH)
    os.makedirs(os.path.join(settings_object.LIBRARY_PATHS[0], "components"))

    # Write a minimal main Sass source importing partial
    source = "\n".join((
        """/* Main sample */""",
        """@import "toinclude";""",
        """#content{ color: red; }""",
    ))
    with open(basedir.join('sass/main.scss').strpath, 'w') as f:
        f.write(source)

    # Write a main Sass source importing minimal source
    source = "\n".join((
        """/* Main importing sample */""",
        """@import "main";""",
    ))
    with open(basedir.join('sass/main_importing.scss').strpath, 'w') as f:
        f.write(source)

    # Write a main Sass source importing library component and partial source
    source = "\n".join((
        """/* Main importing library */""",
        """@import "toinclude";""",
        """@import "components/buttons";""",
    ))
    with open(basedir.join('sass/main_usinglib.scss').strpath, 'w') as f:
        f.write(source)

    # Write a partial Sass source to include
    source = "\n".join((
        """/* Partial source to include */""",
        """.included-partial{ color: gold !important; }""",
    ))
    with open(basedir.join('sass/_toinclude.scss').strpath, 'w') as f:
        f.write(source)

    # Write a partial Sass source to ignore
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


def build_sass_sample_structure(settings_object, basedir):
    """
    Build Sass (indented syntax) sample files structure for handler testing
    """
    # Write needed dirs
    os.makedirs(settings_object.SOURCES_PATH)
    os.makedirs(settings_object.TARGET_PATH)
    os.makedirs(os.path.join(settings_object.LIBRARY_PATHS[0], "components"))

    # Write a minimal main Sass source importing partial
    source = "\n".join((
        """/* Main sample */""",
        """@import toinclude""",
        """#content""",
        """    color: red""",
        "",
    ))
    with open(basedir.join('sass/main.sass').strpath, 'w') as f:
        f.write(source)

    # Write a main Sass source importing minimal source
    source = "\n".join((
        """/* Main importing sample */""",
        """@import main""",
    ))
    with open(basedir.join('sass/main_importing.sass').strpath, 'w') as f:
        f.write(source)

    # Write a main Sass source importing library component and partial source
    source = "\n".join((
        """/* Main importing library */""",
        """@import toinclude""",
        """@import components/buttons""",
    ))
    with open(basedir.join('sass/main_usinglib.sass').strpath, 'w') as f:
        f.write(source)

    # Write a partial Sass source to include
    source = "\n".join((
        """/* Partial source to include */""",
        """.included-partial""",
        """    color: gold !important""",
        "",
    ))
    with open(basedir.join('sass/_toinclude.sass').strpath, 'w') as f:
        f.write(source)

    # Write a partial Sass source to ignore
    source = "\n".join((
        """/* Partial source to ignore because not included */""",
        """.toignore-partial""",
        """    font-weight: bold""",
        "",
    ))
    with open(basedir.join('sass/_notincluded.sass').strpath, 'w') as f:
        f.write(source)

    # Write a main source within library directory
    source = "\n".join((
        """/* Main source for library */""",
        """@import components/buttons""",
    ))
    with open(basedir.join('lib/libmain.sass').strpath, 'w') as f:
        f.write(source)

    # Write a partial source within library directory
    source = "\n".join((
        """/* Buttons component */""",
        """.button""",
        """    display: block""",
        """    border: 1px solid black""",
        """    padding: 5px""",
        "",
    ))
    with open(basedir.join('lib/components/_buttons.sass').strpath, 'w') as f:
        f.write(source)
