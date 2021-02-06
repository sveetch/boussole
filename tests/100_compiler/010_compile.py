# -*- coding: utf-8 -*-
import os
import io

from boussole.conf.model import Settings


def test_001(compiler, temp_builds_dir):
    """
    Basic sample without source map
    """
    basedir = temp_builds_dir.join("compiler_safecompile").strpath

    basic_settings = Settings(initial={
        "SOURCES_PATH": "scss",
        "TARGET_PATH": "css",
        "SOURCE_MAP": False,
        "OUTPUT_STYLES": "compact",
    })

    sourcedir = os.path.join(basedir, basic_settings.SOURCES_PATH)
    targetdir = os.path.join(basedir, basic_settings.TARGET_PATH)

    src = os.path.join(sourcedir, "app.scss")
    dst = os.path.join(targetdir, "app.css")
    src_map = os.path.join(targetdir, "app.map")

    os.makedirs(sourcedir)
    os.makedirs(targetdir)

    # Create sample source to compile
    with io.open(src, "w", encoding="utf-8") as f:
        f.write(
            """#content{
            color: #ff0000;
            font-weight: bold;
            &.foo{ border: 1px solid #000000; }
            }
            """
        )

    # Compile
    success, message = compiler.safe_compile(basic_settings, src, dst)

    assert os.path.exists(dst)
    assert os.path.exists(src_map) is False

    # Assert compiled file is ok
    with io.open(dst, "r", encoding="utf-8") as f:
        content = f.read()

    assert content == (
        """#content { color: #ff0000; font-weight: bold; }\n\n"""
        """#content.foo { border: 1px solid #000000; }\n"""
    )
