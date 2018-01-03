# -*- coding: utf-8 -*-
import pytest


@pytest.mark.parametrize('parser_name,source,expected', [
    # removing singleline comment case 1
    (
        "scss",
        """// foo""",
        "",
    ),
    (
        "sass",
        """// foo""",
        "",
    ),
    # removing singleline comment case 2
    (
        "scss",
        """//foo\n""",
        "",
    ),
    (
        "sass",
        """//foo\n""",
        "",
    ),
    # removing singleline comment case 3
    (
        "scss",
        (
            """\n"""
            """//foo\n"""
        ),
        "",
    ),
    (
        "sass",
        (
            """\n"""
            """//foo\n"""
        ),
        "",
    ),
    # removing singleline comment case 4
    (
        "scss",
        (
            """$foo: true;\n"""
            """// foo\n"""
            """$bar: false;"""
        ),
        """$foo: true;\n$bar: false;""",
    ),
    (
        "sass",
        (
            """$foo: true;\n"""
            """// foo\n"""
            """$bar: false;"""
        ),
        """$foo: true;\n$bar: false;""",
    ),
    # removing singleline comment case 5
    (
        "scss",
        """@import "vendor"; //foo""",
        """@import "vendor";""",
    ),
    (
        "sass",
        """@import "vendor"; //foo""",
        """@import "vendor";""",
    ),
    # removing multiline comment case 1
    (
        "scss",
        """/* foo */""",
        "",
    ),
    (
        "sass",
        """/* foo */""",
        "",
    ),
    # removing multiline comment case 2
    (
        "scss",
        (
            """\n/*\n"""
            """* foo\n"""
            """*/"""
        ),
        "",
    ),
    (
        "sass",
        (
            """\n/*\n"""
            """* foo\n"""
            """*/"""
        ),
        "",
    ),
    # removing multiline comment case 3
    (
        "scss",
        (
            """\n    /*\n"""
            """* foo"""
            """*/"""
            """$bar: true;"""
        ),
        "$bar: true;",
    ),
    (
        "sass",
        (
            """\n    /*\n"""
            """* foo"""
            """*/"""
            """$bar: true;"""
        ),
        "$bar: true;",
    ),
    # removing singleline and multiline comments
    (
        "scss",
        (
            """//Start\n"""
            """/*\n"""
            """ * Pika\n"""
            """ */\n"""
            """$foo: true;\n"""
            """// Boo\n"""
            """$bar: false;\n"""
            """// End"""
        ),
        "$foo: true;\n$bar: false;",
    ),
    (
        "sass",
        (
            """//Start\n"""
            """/*\n"""
            """ * Pika\n"""
            """ */\n"""
            """$foo: true;\n"""
            """// Boo\n"""
            """$bar: false;\n"""
            """// End"""
        ),
        "$foo: true;\n$bar: false;",
    ),
    # trouble with // usage that are not comment
    (
        "scss",
        """@import url("http://foo.bar/dummy");""",
        """@import url("http://foo.bar/dummy");""",
    ),
    (
        "sass",
        """@import url("http://foo.bar/dummy");""",
        """@import url("http://foo.bar/dummy");""",
    ),
    # trouble with // usage that are not comment
    (
        "scss",
        """@import url("http://foo.bar/dummy"); // This is a comment""",
        """@import url("http://foo.bar/dummy");""",
    ),
    (
        "sass",
        """@import url("http://foo.bar/dummy"); // This is a comment""",
        """@import url("http://foo.bar/dummy");""",
    ),
])
def test_remove_001(parsers, parser_name, source, expected):
    parser = parsers[parser_name]
    assert parser.remove_comments(source).strip() == expected
