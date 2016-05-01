# -*- coding: utf-8 -*-
import os
import io
import json
import pytest

from boussole.conf.model import Settings


def test_001(compiler, temp_builds_dir):
    """compiler.SassCompileHelper.safe_compile: Basic sample without source map"""
    basedir = temp_builds_dir.join('compiler_safecompile_001').strpath

    basic_settings = Settings(initial={
        'SOURCES_PATH': 'scss',
        'TARGET_PATH': 'css',
        'SOURCE_MAP': False,
        'OUTPUT_STYLES': 'compact',
    })

    sourcedir = os.path.join(basedir, basic_settings.SOURCES_PATH)
    targetdir = os.path.join(basedir, basic_settings.TARGET_PATH)

    src = os.path.join(sourcedir, "app.scss")
    dst = os.path.join(targetdir, "app.css")
    src_map = os.path.join(targetdir, "app.map")

    os.makedirs(sourcedir)
    os.makedirs(targetdir)

    # Create sample source to compile
    with io.open(src, 'w', encoding='utf-8') as f:
        result = f.write(
            u"""#content{
            color: #ff0000;
            font-weight: bold;
            &.foo{ border: 1px solid #000000; }
            }
            """)

    # Compile
    success, message = compiler.safe_compile(basic_settings, src, dst)

    assert os.path.exists(dst) == True
    assert os.path.exists(src_map) == False

    # Assert compiled file is ok
    with io.open(dst, 'r', encoding='utf-8') as f:
        content = f.read()

    assert content == ("""#content { color: #ff0000; font-weight: bold; }\n\n"""
                      """#content.foo { border: 1px solid #000000; }\n""")

def test_002(compiler, temp_builds_dir):
    """compiler.SassCompileHelper.safe_compile: Same as basic sample but with
       source map"""
    basedir = temp_builds_dir.join('compiler_safecompile_002').strpath

    basic_settings = Settings(initial={
        'SOURCES_PATH': '.',
        'TARGET_PATH': 'css',
        'SOURCE_MAP': True,
        'OUTPUT_STYLES': 'compact',
    })

    sourcedir = os.path.normpath(os.path.join(basedir, basic_settings.SOURCES_PATH))
    targetdir = os.path.normpath(os.path.join(basedir, basic_settings.TARGET_PATH))

    os.makedirs(sourcedir)
    os.makedirs(targetdir)

    src = os.path.join(sourcedir, "app.scss")
    dst = os.path.join(targetdir, "app.css")
    src_map = os.path.join(targetdir, "app.map")

    # Create sample source to compile
    with io.open(src, 'w', encoding='utf-8') as f:
        result = f.write(u"""#content{ color:#ff0000; font-weight:bold; }""")

    # Compile
    success, message = compiler.safe_compile(basic_settings, src, dst)

    assert os.path.exists(dst) == True
    assert os.path.exists(src_map) == True

    with io.open(dst, 'r', encoding='utf-8') as f:
        content = f.read()

    with io.open(src_map, 'r', encoding='utf-8') as f:
        sourcemap = json.load(f)

    #print content
    #print "."*60
    #print sourcemap

    # Assert compiled file is ok
    assert content == ("""#content { color: #ff0000; font-weight: bold; }\n\n"""
                      """/*# sourceMappingURL=css/app.map */""")

    # Assert sourcemap is ok
    # Drop 'version' key since it will cause problem with futur libsass
    # versions
    del sourcemap['version']
    # Assert source map is ok
    assert sourcemap == {
        "file": "../app.css",
        "sources": [
                "../app.scss"
        ],
        "mappings": ("AAAA,AAAA,QAAQ,CAAA,EAAE,KAAK,EAAC,OAAQ,EAAE,WAAW,EAAC,"
                     "IAAK,GAAI"),
        "names": []
    }

