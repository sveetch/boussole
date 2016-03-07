# -*- coding: utf-8 -*-
import pytest


def test_parser_comment_remove_001(settings, parser):
    """parser.ScssImportsParser: removing singleline comment case 1"""
    assert parser.remove_comments("""// foo""") == ""


def test_parser_comment_remove_002(settings, parser):
    """parser.ScssImportsParser: removing singleline comment case 2"""
    assert parser.remove_comments("""//foo
        """).strip() == ""


def test_parser_comment_remove_003(settings, parser):
    """parser.ScssImportsParser: removing singleline comment case 3"""
    assert parser.remove_comments("""
        //foo
    """).strip() == ""


def test_parser_comment_remove_004(settings, parser):
    """parser.ScssImportsParser: removing singleline comment case 4"""
    assert parser.remove_comments("""$foo: true;
// foo
$bar: false;
""").strip() == """$foo: true;\n$bar: false;"""


def test_parser_comment_remove_005(settings, parser):
    """parser.ScssImportsParser: removing singleline comment case 5"""
    results = parser.remove_comments("""@import "vendor"; //foo""").strip()
    assert results == """@import "vendor";"""


def test_parser_comment_remove_006(settings, parser):
    """parser.ScssImportsParser: removing multiline comment case 1"""
    assert parser.remove_comments("""/* foo */""") == ""


def test_parser_comment_remove_007(settings, parser):
    """parser.ScssImportsParser: removing multiline comment case 2"""
    assert parser.remove_comments("""
        /* 
            * foo
            */""").strip() == ""


def test_parser_comment_remove_008(settings, parser):
    """parser.ScssImportsParser: removing multiline comment case 3"""
    assert parser.remove_comments("""
        /* 
            * foo
            */
            $bar: true;""").strip() == "$bar: true;"


def test_parser_comment_remove_009(settings, parser):
    """parser.ScssImportsParser: removing singleline and multiline comments"""
    assert parser.remove_comments("""//Start
/* 
 * Pika
 */
$foo: true;
// Boo
$bar: false;
// End""").strip() == "$foo: true;\n$bar: false;"
