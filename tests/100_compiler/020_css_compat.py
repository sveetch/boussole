# -*- coding: utf-8 -*-
import os
import io
import pytest

from boussole.conf.model import Settings


def test_css_compat_ok(compiler, temp_builds_dir):
    """
    Ensure CSS import compatibility is ok
    """
    basedir = temp_builds_dir.join('compiler_css_compat_ok').strpath

    basic_settings = Settings(initial={
        'SOURCES_PATH': 'scss',
        'TARGET_PATH': 'css',
        'SOURCE_MAP': False,
        'OUTPUT_STYLES': 'compact',
    })

    sourcedir = os.path.join(basedir, basic_settings.SOURCES_PATH)
    targetdir = os.path.join(basedir, basic_settings.TARGET_PATH)

    src = os.path.join(sourcedir, "app.scss")
    css_include = os.path.join(sourcedir, "_dummy.css")
    dst = os.path.join(targetdir, "app.css")

    os.makedirs(sourcedir)
    os.makedirs(targetdir)

    # Create sample main Sass source
    with io.open(src, 'w', encoding='utf-8') as f:
        result = f.write(
            u"""
            @import "dummy";
            #content{
            color: #ff0000;
            font-weight: bold;
            &.foo{ border: 1px solid #000000; }
            }
            """)

    # Create sample main Sass source
    with io.open(css_include, 'w', encoding='utf-8') as f:
        result = f.write(
            u"""
            .dummy{
                color: #00ff00;
            }
            """)

    # Compile
    success, message = compiler.safe_compile(basic_settings, src, dst)

    assert os.path.exists(dst) == True

    # Assert compiled file is ok
    with io.open(dst, 'r', encoding='utf-8') as f:
        content = f.read()

    attempted = (""".dummy { color: #00ff00; }\n\n"""
                 """#content { color: #ff0000; font-weight: bold; }\n\n"""
                 """#content.foo { border: 1px solid #000000; }\n""")

    assert content == attempted
