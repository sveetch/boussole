# -*- coding: utf-8 -*-
import os
import io
import json

from boussole.conf.model import Settings


def test_source_map_path_001(compiler, temp_builds_dir):
    """
    Check about source map path from 'sourceMappingURL' with a simple path
    """
    basic_settings = Settings(initial={
        'SOURCES_PATH': '.',
        'TARGET_PATH': 'css',
        'SOURCE_MAP': True,
        'OUTPUT_STYLES': 'compact',
    })

    basedir = temp_builds_dir.join('compiler_source_map_path_001').strpath
    sourcedir = os.path.normpath(
        os.path.join(basedir, basic_settings.SOURCES_PATH)
    )
    targetdir = os.path.normpath(
        os.path.join(basedir, basic_settings.TARGET_PATH)
    )

    os.makedirs(sourcedir)
    os.makedirs(targetdir)

    src = os.path.join(sourcedir, "app.scss")
    dst = os.path.join(targetdir, "app.css")
    src_map = os.path.join(targetdir, "app.map")

    # Create sample source to compile
    with io.open(src, 'w', encoding='utf-8') as f:
        f.write(u"""#content{ color:#ff0000; font-weight:bold; }""")

    # Compile
    success, message = compiler.safe_compile(basic_settings, src, dst)

    assert os.path.exists(dst)
    assert os.path.exists(src_map)

    with io.open(dst, 'r', encoding='utf-8') as f:
        content = f.read()

    with io.open(src_map, 'r', encoding='utf-8') as f:
        sourcemap = json.load(f)

    # Assert compiled file is ok
    assert content == (
        """#content { color: #ff0000; font-weight: bold; }\n\n"""
        """/*# sourceMappingURL=app.map */"""
    )

    # Drop keys we don't care for this test
    del sourcemap['version']
    del sourcemap['mappings']
    del sourcemap['names']

    # Assert source map is ok
    assert sourcemap == {
        "file": "app.css",
        "sources": [
                "../app.scss"
        ],
    }


def test_source_map_path_002(compiler, temp_builds_dir):
    """
    Check about source map path from 'sourceMappingURL' with CSS dir below
    Sass source dir
    """
    basic_settings = Settings(initial={
        'SOURCES_PATH': 'scss',
        'TARGET_PATH': 'project/css',
        'SOURCE_MAP': True,
        'OUTPUT_STYLES': 'compact',
    })

    basedir = temp_builds_dir.join('compiler_source_map_path_002').strpath
    sourcedir = os.path.normpath(
        os.path.join(basedir, basic_settings.SOURCES_PATH)
    )
    targetdir = os.path.normpath(
        os.path.join(basedir, basic_settings.TARGET_PATH)
    )

    os.makedirs(sourcedir)
    os.makedirs(targetdir)

    src = os.path.join(sourcedir, "app.scss")
    dst = os.path.join(targetdir, "app.css")
    src_map = os.path.join(targetdir, "app.map")

    # Create sample source to compile
    with io.open(src, 'w', encoding='utf-8') as f:
        f.write(u"""#content{ color:#ff0000; font-weight:bold; }""")

    # Compile
    success, message = compiler.safe_compile(basic_settings, src, dst)

    assert os.path.exists(dst)
    assert os.path.exists(src_map)

    with io.open(dst, 'r', encoding='utf-8') as f:
        content = f.read()

    with io.open(src_map, 'r', encoding='utf-8') as f:
        sourcemap = json.load(f)

    # Assert compiled file is ok
    assert content == (
        """#content { color: #ff0000; font-weight: bold; }\n\n"""
        """/*# sourceMappingURL=app.map */"""
    )

    # Drop keys we don't care for this test
    del sourcemap['version']
    del sourcemap['mappings']
    del sourcemap['names']

    # Assert source map is ok
    assert sourcemap == {
        "file": "app.css",
        "sources": [
                "../../scss/app.scss"
        ],
    }


def test_source_map_content(compiler, temp_builds_dir):
    """
    Check about source map content
    """
    basic_settings = Settings(initial={
        'SOURCES_PATH': '.',
        'TARGET_PATH': 'css',
        'SOURCE_MAP': True,
        'OUTPUT_STYLES': 'compact',
    })

    basedir = temp_builds_dir.join('compiler_source_map_content').strpath

    sourcedir = os.path.normpath(os.path.join(basedir, basic_settings.SOURCES_PATH))
    targetdir = os.path.normpath(os.path.join(basedir, basic_settings.TARGET_PATH))

    os.makedirs(sourcedir)
    os.makedirs(targetdir)

    src = os.path.join(sourcedir, "app.scss")
    dst = os.path.join(targetdir, "app.css")
    src_map = os.path.join(targetdir, "app.map")

    # Create sample source to compile
    with io.open(src, 'w', encoding='utf-8') as f:
        f.write(u"""#content{ color:#ff0000; font-weight:bold; }""")

    # Compile
    success, message = compiler.safe_compile(basic_settings, src, dst)

    assert os.path.exists(dst)
    assert os.path.exists(src_map)

    with io.open(dst, 'r', encoding='utf-8') as f:
        content = f.read()

    with io.open(src_map, 'r', encoding='utf-8') as f:
        sourcemap = json.load(f)

    # Assert compiled file is ok
    assert content == (
        """#content { color: #ff0000; font-weight: bold; }\n\n"""
        """/*# sourceMappingURL=app.map */"""
    )

    # Drop 'version' key since it will cause problem with futur libsass
    # versions
    del sourcemap['version']

    # Assert source map is ok
    assert sourcemap == {
        "file": "app.css",
        "sources": [
                "../app.scss"
        ],
        "mappings": ("AAAA,AAAA,QAAQ,CAAA,EAAE,KAAK,EAAC,OAAO,EAAE,WAAW,EAAC,"
                     "IAAI,GAAI"),
        "names": []
    }
