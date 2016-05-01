# -*- coding: utf-8 -*-
import os
import logging
import pytest

from boussole.exceptions import UnresolvablePath

from utils import (DummyBaseEvent, DummyMoveEvent, DummyBaseHandler,
                   UnitTestableLibraryEventHandler,
                   UnitTestableProjectEventHandler, start_env,
                   build_sample_structure)


def test_index_001(caplog, temp_builds_dir):
    """watcher.SassProjectEventHandler: UnresolvablePath on index from 'on_any_event'"""
    basedir = temp_builds_dir.join('watcher_fails_001')

    bdir, logger, inspector, settings_object, watcher_opts = start_env(basedir)

    build_sample_structure(settings_object, basedir)

    # Init handler
    project_handler = UnitTestableProjectEventHandler(
        settings_object,
        logger,
        inspector,
        **watcher_opts
    )

    #with pytest.raises(UnresolvablePath):
    # First indexing is a success
    project_handler.on_any_event(object())

    # Write some error file
    source = "\n".join((
        """/* New main source */""",
        """@import "idontexist";""",
    ))
    with open(basedir.join('sass/error_main.scss').strpath, 'w') as f:
        f.write(source)

    # Second indexing raise exception but catched
    project_handler.on_any_event(object())

    # Error from core API is catched
    assert project_handler._event_error == True
    # Logged error
    assert caplog.record_tuples == [
        (
            'boussole',
            40,
            "Imported path 'idontexist' does not exist in '{}'".format(basedir.join('sass').strpath)
        )
    ]


def test_deleted_001(caplog, temp_builds_dir):
    """watcher.SassProjectEventHandler: UnresolvablePath on 'Deleted' event for a partial
       source included by other files"""
    basedir = temp_builds_dir.join('watcher_fails_041')

    bdir, logger, inspector, settings_object, watcher_opts = start_env(basedir)

    build_sample_structure(settings_object, basedir)

    # Init handler
    project_handler = UnitTestableProjectEventHandler(
        settings_object,
        logger,
        inspector,
        **watcher_opts
    )

    os.remove(bdir('sass/_toinclude.scss'))

    # Error is catched
    project_handler.on_deleted(DummyBaseEvent(bdir('sass/_toinclude.scss')))

    # Error from core API is catched
    assert project_handler._event_error == True
    # Logged error
    assert caplog.record_tuples == [
        (
            'boussole',
            40,
            "Imported path 'toinclude' does not exist in '{}'".format(basedir.join('sass').strpath)
        )
    ]
