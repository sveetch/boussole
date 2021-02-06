# -*- coding: utf-8 -*-
import io


def test_001(compiler, temp_builds_dir):
    """
    Just creating file with latin content
    """
    filepath = temp_builds_dir.join("compiler_write_001")

    content = """Some sample latin text"""

    compiler.write_content(content, filepath.strpath)

    # Read file to compare
    with io.open(filepath.strpath, "r", encoding="utf-8") as f:
        result = f.read()

    assert content == result


def test_002(compiler, temp_builds_dir):
    """
    Creating file with unicode content
    """
    filepath = temp_builds_dir.join("compiler_write_002")

    content = """Some sample unicode text: フランス Furansu"""

    compiler.write_content(content, filepath.strpath)

    # Read file to compare
    with io.open(filepath.strpath, "r", encoding="utf-8") as f:
        result = f.read()

    assert content == result


def test_003(compiler, temp_builds_dir):
    """
    Creating file into subdirectory
    """
    filepath = temp_builds_dir.join("foo/bar/home.txt")

    content = """Some sample unicode text: フランス Furansu"""

    compiler.write_content(content, filepath.strpath)

    # Read file to compare
    with io.open(filepath.strpath, "r", encoding="utf-8") as f:
        result = f.read()

    assert content == result
