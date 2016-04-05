# -*- coding: utf-8 -*-
import os
import logging
import pytest

from boussole.exceptions import UnresolvablePath

from utils import (DummyBaseEvent, DummyMoveEvent, DummyBaseHandler,
                   UnitTestableLibraryEventHandler,
                   UnitTestableProjectEventHandler, start_env,
                   build_sample_structure)


def test_watcher_project_compilablefiles_001(settings, temp_builds_dir):
    """watcher.SassProjectEventHandler: Testing 'handler.compilable_files' return"""
    basedir = temp_builds_dir.join('watcher_001')

    bdir, logger, inspector, settings_object, watcher_opts = start_env(basedir)

    build_sample_structure(settings_object, basedir)

    # Init handler
    project_handler = UnitTestableProjectEventHandler(
        settings_object,
        logger,
        inspector,
        **watcher_opts
    )

    # Manually call on_any_event since we directly access to
    # 'handler.compilable_files' bypassing the event hierarchy
    project_handler.on_any_event(object())

    assert project_handler.compilable_files == {
        bdir('sass/main.scss'): bdir('css/main.css'),
        bdir('sass/main_importing.scss'): bdir('css/main_importing.css'),
        bdir('sass/main_usinglib.scss'): bdir('css/main_usinglib.css'),
    }


def test_watcher_project_move_010(settings, temp_builds_dir):
    """watcher.SassProjectEventHandler: 'Move' event on main sample"""
    basedir = temp_builds_dir.join('watcher_010')

    bdir, logger, inspector, settings_object, watcher_opts = start_env(basedir)

    build_sample_structure(settings_object, basedir)

    # Init handler
    project_handler = UnitTestableProjectEventHandler(
        settings_object,
        logger,
        inspector,
        **watcher_opts
    )

    project_handler.on_moved(DummyMoveEvent(bdir('sass/main.scss')))
    assert os.listdir(basedir.join("css").strpath) == ['main.css', 'main_importing.css']


def test_watcher_project_move_011(settings, temp_builds_dir):
    """watcher.SassProjectEventHandler: 'Move' event from a source depending from
       main sample"""
    basedir = temp_builds_dir.join('watcher_011')

    bdir, logger, inspector, settings_object, watcher_opts = start_env(basedir)

    build_sample_structure(settings_object, basedir)

    # Init handler
    project_handler = UnitTestableProjectEventHandler(
        settings_object,
        logger,
        inspector,
        **watcher_opts
    )

    project_handler.on_moved(DummyMoveEvent(bdir('sass/main_importing.scss')))
    assert os.listdir(basedir.join("css").strpath) == ['main_importing.css']


def test_watcher_project_move_012(settings, temp_builds_dir):
    """watcher.SassProjectEventHandler: 'Move' event on included partial
       source"""
    basedir = temp_builds_dir.join('watcher_012')

    bdir, logger, inspector, settings_object, watcher_opts = start_env(basedir)

    build_sample_structure(settings_object, basedir)

    # Init handler
    project_handler = UnitTestableProjectEventHandler(
        settings_object,
        logger,
        inspector,
        **watcher_opts
    )

    project_handler.on_moved(DummyMoveEvent(bdir('sass/_toinclude.scss')))
    assert os.listdir(basedir.join("css").strpath) == ['main_usinglib.css', 'main.css', 'main_importing.css']


def test_watcher_project_modified_020(settings, temp_builds_dir):
    """watcher.SassProjectEventHandler: 'Modified' event on included partial
       source"""
    basedir = temp_builds_dir.join('watcher_020')

    bdir, logger, inspector, settings_object, watcher_opts = start_env(basedir)

    build_sample_structure(settings_object, basedir)

    # Init handler
    project_handler = UnitTestableProjectEventHandler(
        settings_object,
        logger,
        inspector,
        **watcher_opts
    )

    project_handler.on_modified(DummyBaseEvent(bdir('sass/_toinclude.scss')))
    assert os.listdir(basedir.join("css").strpath) == ['main_usinglib.css', 'main.css', 'main_importing.css']


def test_watcher_project_created_030(settings, temp_builds_dir):
    """watcher.SassProjectEventHandler: 'Created' event for a new main source"""
    basedir = temp_builds_dir.join('watcher_030')

    bdir, logger, inspector, settings_object, watcher_opts = start_env(basedir)

    build_sample_structure(settings_object, basedir)

    # Init handler
    project_handler = UnitTestableProjectEventHandler(
        settings_object,
        logger,
        inspector,
        **watcher_opts
    )

    # Write a new main source
    source = "\n".join((
        """/* New main source */""",
        """#content{ padding: 10px; margin: 5px 0; }""",
    ))
    with open(basedir.join('sass/new_main.scss').strpath, 'w') as f:
        f.write(source)

    project_handler.on_created(DummyBaseEvent(bdir('sass/new_main.scss')))
    assert os.listdir(basedir.join("css").strpath) == ['new_main.css']


def test_watcher_project_deleted_040(settings, temp_builds_dir):
    """watcher.SassProjectEventHandler: 'Deleted' event for a main source"""
    basedir = temp_builds_dir.join('watcher_040')

    bdir, logger, inspector, settings_object, watcher_opts = start_env(basedir)

    build_sample_structure(settings_object, basedir)

    # Init handler
    project_handler = UnitTestableProjectEventHandler(
        settings_object,
        logger,
        inspector,
        **watcher_opts
    )

    os.remove(bdir('sass/main_importing.scss'))

    project_handler.on_deleted(DummyBaseEvent(bdir('sass/main_importing.scss')))
    assert os.listdir(basedir.join("css").strpath) == []


def test_watcher_project_deleted_041(settings, temp_builds_dir):
    """watcher.SassProjectEventHandler: 'Deleted' event for a partial source
       included by other files"""
    basedir = temp_builds_dir.join('watcher_041')

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

    with pytest.raises(UnresolvablePath):
        project_handler.on_deleted(DummyBaseEvent(bdir('sass/_toinclude.scss')))


def test_watcher_project_whole_050(settings, temp_builds_dir):
    """watcher.SassProjectEventHandler: Routine using some events on various
       sources"""
    basedir = temp_builds_dir.join('watcher_050')

    bdir, logger, inspector, settings_object, watcher_opts = start_env(basedir)

    build_sample_structure(settings_object, basedir)

    # Init handler
    project_handler = UnitTestableProjectEventHandler(
        settings_object,
        logger,
        inspector,
        **watcher_opts
    )

    # Modify a partial source
    project_handler.on_modified(DummyBaseEvent(bdir('sass/_toinclude.scss')))
    assert os.listdir(basedir.join("css").strpath) == ['main_usinglib.css', 'main.css', 'main_importing.css']

    # Create a new main source
    source = "\n".join((
        """/* New main source */""",
        """#content{ padding: 10px; margin: 5px 0; }""",
    ))
    with open(basedir.join('sass/new_main.scss').strpath, 'w') as f:
        f.write(source)

    project_handler.on_created(DummyBaseEvent(bdir('sass/new_main.scss')))
    assert os.listdir(basedir.join("css").strpath) == ['new_main.css', 'main_usinglib.css', 'main.css', 'main_importing.css']

    # Delete a main source
    os.remove(bdir('css/main_importing.css'))
    os.remove(bdir('sass/main_importing.scss'))

    project_handler.on_deleted(DummyBaseEvent(bdir('sass/main_importing.scss')))
    assert os.listdir(basedir.join("css").strpath) == ['new_main.css', 'main_usinglib.css', 'main.css']

    # Simulate moved source
    project_handler.on_moved(DummyMoveEvent(bdir('sass/_toinclude.scss')))
    assert os.listdir(basedir.join("css").strpath) == ['new_main.css', 'main_usinglib.css', 'main.css']


def test_watcher_library_modified_101(settings, temp_builds_dir):
    """watcher.SassLibraryEventHandler: 'Modified' event on a library
       component"""
    basedir = temp_builds_dir.join('watcher_101')

    bdir, logger, inspector, settings_object, watcher_opts = start_env(basedir)

    build_sample_structure(settings_object, basedir)

    # Init handler
    project_handler = UnitTestableLibraryEventHandler(
        settings_object,
        logger,
        inspector,
        **watcher_opts
    )

    project_handler.on_modified(DummyBaseEvent(bdir('lib/components/_buttons.scss')))

    project_handler.on_modified(DummyBaseEvent(bdir('lib/libmain.scss')))

    # Almost dummy validation because on wrong behavior (with
    # UnitTestableProjectEventHandler instead of
    # UnitTestableLibraryEventHandler) CSS files are writed to "../lib"
    # path, that is under the "css" dir.
    assert os.listdir(basedir.join("css").strpath) == ['main_usinglib.css']
