# -*- coding: utf-8 -*-
import os

from utils import (DummyBaseEvent, DummyMoveEvent, UnitTestableLibraryEventHandler,
                   UnitTestableProjectEventHandler, start_env,
                   build_scss_sample_structure, build_sass_sample_structure)


def test_compilablefiles_scss(temp_builds_dir):
    """
    Testing 'handler.compilable_files' return the right paths with *.scss files
    """
    basedir = temp_builds_dir.join('watcher_success_001')

    bdir, inspector, settings_object, watcher_opts = start_env(basedir)

    build_scss_sample_structure(settings_object, basedir)

    # Init handler
    project_handler = UnitTestableProjectEventHandler(
        settings_object,
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


def test_compilablefiles_sass(temp_builds_dir):
    """
    Testing 'handler.compilable_files' return the right paths with *.sass files
    """
    basedir = temp_builds_dir.join('watcher_success_002')

    bdir, inspector, settings_object, watcher_opts = start_env(basedir)

    build_sass_sample_structure(settings_object, basedir)

    # Init handler
    project_handler = UnitTestableProjectEventHandler(
        settings_object,
        inspector,
        **watcher_opts
    )

    # Manually call on_any_event since we directly access to
    # 'handler.compilable_files' bypassing the event hierarchy
    project_handler.on_any_event(object())

    assert project_handler.compilable_files == {
        bdir('sass/main.sass'): bdir('css/main.css'),
        bdir('sass/main_importing.sass'): bdir('css/main_importing.css'),
        bdir('sass/main_usinglib.sass'): bdir('css/main_usinglib.css'),
    }


def test_move_scss_010(temp_builds_dir):
    """
    'Move' event on main sample
    """
    basedir = temp_builds_dir.join('watcher_move_scss_010')

    bdir, inspector, settings_object, watcher_opts = start_env(basedir)

    build_scss_sample_structure(settings_object, basedir)

    # Init handler
    project_handler = UnitTestableProjectEventHandler(
        settings_object,
        inspector,
        **watcher_opts
    )

    project_handler.on_moved(DummyMoveEvent(bdir('sass/main.scss')))

    results = os.listdir(basedir.join("css").strpath)
    results.sort()

    assert results == [
        'main.css',
        'main_importing.css'
    ]


def test_move_sass_010(temp_builds_dir):
    """
    'Move' event on main sample
    """
    basedir = temp_builds_dir.join('watcher_move_sass_010')

    bdir, inspector, settings_object, watcher_opts = start_env(basedir)

    build_sass_sample_structure(settings_object, basedir)

    # Init handler
    project_handler = UnitTestableProjectEventHandler(
        settings_object,
        inspector,
        **watcher_opts
    )

    project_handler.on_moved(DummyMoveEvent(bdir('sass/main.sass')))

    results = os.listdir(basedir.join("css").strpath)
    results.sort()

    assert results == [
        'main.css',
        'main_importing.css'
    ]


def test_move_scss_011(temp_builds_dir):
    """
    'Move' event from a source depending from main sample
    """
    basedir = temp_builds_dir.join('watcher_move_scss_011')

    bdir, inspector, settings_object, watcher_opts = start_env(basedir)

    build_scss_sample_structure(settings_object, basedir)

    # Init handler
    project_handler = UnitTestableProjectEventHandler(
        settings_object,
        inspector,
        **watcher_opts
    )

    project_handler.on_moved(DummyMoveEvent(bdir('sass/main_importing.scss')))

    results = os.listdir(basedir.join("css").strpath)
    results.sort()

    assert results == [
        'main_importing.css'
    ]


def test_move_scss_012(temp_builds_dir):
    """'Move' event on included partial
       source"""
    basedir = temp_builds_dir.join('watcher_move_scss_012')

    bdir, inspector, settings_object, watcher_opts = start_env(basedir)

    build_scss_sample_structure(settings_object, basedir)

    # Init handler
    project_handler = UnitTestableProjectEventHandler(
        settings_object,
        inspector,
        **watcher_opts
    )

    project_handler.on_moved(DummyMoveEvent(bdir('sass/_toinclude.scss')))

    results = os.listdir(basedir.join("css").strpath)
    results.sort()

    assert results == [
        'main.css',
        'main_importing.css',
        'main_usinglib.css',
    ]


def test_modified_020(temp_builds_dir):
    """
    'Modified' event on included partial source
    """
    basedir = temp_builds_dir.join('watcher_success_020')

    bdir, inspector, settings_object, watcher_opts = start_env(basedir)

    build_scss_sample_structure(settings_object, basedir)

    # Init handler
    project_handler = UnitTestableProjectEventHandler(
        settings_object,
        inspector,
        **watcher_opts
    )

    project_handler.on_modified(DummyBaseEvent(bdir('sass/_toinclude.scss')))

    results = os.listdir(basedir.join("css").strpath)
    results.sort()

    assert results == [
        'main.css',
        'main_importing.css',
        'main_usinglib.css',
    ]


def test_created_030(temp_builds_dir):
    """
    'Created' event for a new main source
    """
    basedir = temp_builds_dir.join('watcher_success_030')

    bdir, inspector, settings_object, watcher_opts = start_env(basedir)

    build_scss_sample_structure(settings_object, basedir)

    # Init handler
    project_handler = UnitTestableProjectEventHandler(
        settings_object,
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

    results = os.listdir(basedir.join("css").strpath)
    results.sort()

    assert results == [
        'new_main.css',
    ]


def test_deleted_040(temp_builds_dir):
    """
    'Deleted' event for a main source
    """
    basedir = temp_builds_dir.join('watcher_success_040')

    bdir, inspector, settings_object, watcher_opts = start_env(basedir)

    build_scss_sample_structure(settings_object, basedir)

    # Init handler
    project_handler = UnitTestableProjectEventHandler(
        settings_object,
        inspector,
        **watcher_opts
    )

    os.remove(bdir('sass/main_importing.scss'))

    project_handler.on_deleted(DummyBaseEvent(bdir('sass/main_importing.scss')))

    results = os.listdir(basedir.join("css").strpath)
    results.sort()

    assert results == []


def test_whole_050(temp_builds_dir):
    """
    Routine using some events on various sources
    """
    basedir = temp_builds_dir.join('watcher_success_050')

    bdir, inspector, settings_object, watcher_opts = start_env(basedir)

    build_scss_sample_structure(settings_object, basedir)

    # Init handler
    project_handler = UnitTestableProjectEventHandler(
        settings_object,
        inspector,
        **watcher_opts
    )

    # Modify a partial source
    project_handler.on_modified(DummyBaseEvent(bdir('sass/_toinclude.scss')))

    results = os.listdir(basedir.join("css").strpath)
    results.sort()

    assert results == [
        'main.css',
        'main_importing.css',
        'main_usinglib.css',
    ]

    # Create a new main source
    source = "\n".join((
        """/* New main source */""",
        """#content{ padding: 10px; margin: 5px 0; }""",
    ))
    with open(basedir.join('sass/new_main.scss').strpath, 'w') as f:
        f.write(source)

    project_handler.on_created(DummyBaseEvent(bdir('sass/new_main.scss')))

    results = os.listdir(basedir.join("css").strpath)
    results.sort()

    assert results == [
        'main.css',
        'main_importing.css',
        'main_usinglib.css',
        'new_main.css',
    ]

    # Delete a main source
    os.remove(bdir('css/main_importing.css'))
    os.remove(bdir('sass/main_importing.scss'))

    project_handler.on_deleted(DummyBaseEvent(bdir('sass/main_importing.scss')))

    results = os.listdir(basedir.join("css").strpath)
    results.sort()

    assert results == [
        'main.css',
        'main_usinglib.css',
        'new_main.css',
    ]

    # Simulate moved source
    project_handler.on_moved(DummyMoveEvent(bdir('sass/_toinclude.scss')))

    results = os.listdir(basedir.join("css").strpath)
    results.sort()

    assert results == [
        'main.css',
        'main_usinglib.css',
        'new_main.css',
    ]


def test_library_modified_101(temp_builds_dir):
    """
    'Modified' event on a library component
    """
    basedir = temp_builds_dir.join('watcher_success_101')

    bdir, inspector, settings_object, watcher_opts = start_env(basedir)

    build_scss_sample_structure(settings_object, basedir)

    # Init handler
    project_handler = UnitTestableLibraryEventHandler(
        settings_object,
        inspector,
        **watcher_opts
    )

    project_handler.on_modified(DummyBaseEvent(bdir('lib/components/_buttons.scss')))

    project_handler.on_modified(DummyBaseEvent(bdir('lib/libmain.scss')))

    results = os.listdir(basedir.join("css").strpath)
    results.sort()

    # Almost dummy validation because on wrong behavior (with
    # UnitTestableProjectEventHandler instead of
    # UnitTestableLibraryEventHandler) CSS files are writed to "../lib"
    # path, that is under the "css" dir.
    assert results == [
        'main_usinglib.css',
    ]
