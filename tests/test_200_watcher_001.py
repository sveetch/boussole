# -*- coding: utf-8 -*-
"""
TODO: Better should use pytest tmpdir by function mode instead of click
      isolation.
"""
import os

import pytest

import click
from click.testing import CliRunner

from utils import (DummyBaseEvent, DummyMoveEvent, DummyBaseHandler,
                   UnitTestableLibraryEventHandler,
                   UnitTestableProjectEventHandler, start_env,
                   build_sample_structure)


def test_watcher_project_compilablefiles_001(settings):
    """watcher.SassProjectEventHandler: Testing 'handler.compilable_files' return"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        basedir = os.getcwd()
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


def test_watcher_project_move_010(settings):
    """watcher.SassProjectEventHandler: 'Move' event on main sample"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        basedir = os.getcwd()
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
        assert os.listdir("css") == ['main.css', 'main_importing.css']


def test_watcher_project_move_011(settings):
    """watcher.SassProjectEventHandler: 'Move' event from a source depending from
       main sample"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        basedir = os.getcwd()
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
        assert os.listdir("css") == ['main_importing.css']


def test_watcher_project_move_012(settings):
    """watcher.SassProjectEventHandler: 'Move' event on included partial
       source"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        basedir = os.getcwd()
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
        assert os.listdir("css") == ['main_usinglib.css', 'main.css', 'main_importing.css']


def test_watcher_project_modified_020(settings):
    """watcher.SassProjectEventHandler: 'Modified' event on included partial
       source"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        basedir = os.getcwd()
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
        assert os.listdir("css") == ['main_usinglib.css', 'main.css', 'main_importing.css']


def test_watcher_project_created_030(settings):
    """watcher.SassProjectEventHandler: 'Created' event for a new main source"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        basedir = os.getcwd()
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
        with open('sass/new_main.scss', 'w') as f:
            f.write(source)

        project_handler.on_created(DummyBaseEvent(bdir('sass/new_main.scss')))
        assert os.listdir("css") == ['new_main.css']


def test_watcher_project_deleted_040(settings):
    """watcher.SassProjectEventHandler: 'Deleted' event for a main source"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        basedir = os.getcwd()
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
        assert os.listdir("css") == []


#def test_watcher_project_whole_050(settings):
    #"""watcher.SassProjectEventHandler: Routine using some events on various
       #sources"""
    #runner = CliRunner()
    #with runner.isolated_filesystem():
        #basedir = os.getcwd()
        #bdir, logger, inspector, settings_object, watcher_opts = start_env(basedir)

        #build_sample_structure(settings_object, basedir)

        ## Init handler
        #project_handler = UnitTestableProjectEventHandler(
            #settings_object,
            #logger,
            #inspector,
            #**watcher_opts
        #)

        #os.remove(bdir('sass/main_importing.scss'))

        #project_handler.on_deleted(DummyBaseEvent(bdir('sass/main_importing.scss')))
        #assert os.listdir("css") == []

        #assert 1 == 42


def test_watcher_library_modified_101(settings):
    """watcher.SassLibraryEventHandler: 'Modified' event on a library
       component"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        basedir = os.getcwd()
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
        assert os.listdir("css") == ['main_usinglib.css']
