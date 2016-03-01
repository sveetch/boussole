# -*- coding: utf-8 -*-
import pytest


def test_parser_010_remove_comment(settings, parser):
    """parser.ScssImportsParser: removing singleline comment case 1"""
    assert parser.remove_comments("""// foo""") == ""

def test_parser_011_remove_comment(settings, parser):
    """parser.ScssImportsParser: removing singleline comment case 2"""
    assert parser.remove_comments("""//foo
        """).strip() == ""

def test_parser_012_remove_comment(settings, parser):
    """parser.ScssImportsParser: removing singleline comment case 3"""
    assert parser.remove_comments("""
        //foo
    """).strip() == ""

def test_parser_013_remove_comment(settings, parser):
    """parser.ScssImportsParser: removing singleline comment case 4"""
    assert parser.remove_comments("""$foo: true;
// foo
$bar: false;
""").strip() == """$foo: true;\n$bar: false;"""

def test_parser_014_remove_comment(settings, parser):
    """parser.ScssImportsParser: removing singleline comment case 5"""
    assert parser.remove_comments("""@import "vendor"; //foo""").strip() == """@import "vendor";"""

def test_parser_015_remove_comment(settings, parser):
    """parser.ScssImportsParser: removing multiline comment case 1"""
    assert parser.remove_comments("""/* foo */""") == ""

def test_parser_016_remove_comment(settings, parser):
    """parser.ScssImportsParser: removing multiline comment case 2"""
    assert parser.remove_comments("""
        /* 
            * foo
            */""").strip() == ""

def test_parser_017_remove_comment(settings, parser):
    """parser.ScssImportsParser: removing multiline comment case 3"""
    assert parser.remove_comments("""
        /* 
            * foo
            */
            $bar: true;""").strip() == "$bar: true;"

def test_parser_018_remove_comment(settings, parser):
    """parser.ScssImportsParser: removing singleline and multiline comments"""
    assert parser.remove_comments("""//Start
/* 
 * Pika
 */
$foo: true;
// Boo
$bar: false;
// End""").strip() == "$foo: true;\n$bar: false;"
