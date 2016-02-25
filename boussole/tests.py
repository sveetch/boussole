# -*- coding: utf-8 -*-
"""
Unittests

TODO: Parser is bugged with commented import.
"""
import os, unittest

import boussole
from boussole.parser import ScssImportsParser
from boussole.resolver import ImportPathsResolver

class case_01_ParserTestCase(unittest.TestCase):
    """Unittest to parse import rules"""
    
    def setUp(self):
        self.debug = False
        self.parser = ScssImportsParser()
        self.fixtures_dir = os.path.join(os.path.abspath(os.path.dirname(boussole.__file__)), 'test_fixtures')
    
    def dummy_output(self, content):
        # Just output something to print for debugguing
        if self.debug:
            print content
    
    
    def test_001_unquote1(self):
        """parser.ScssImportsParser: unquote case 1"""
        self.assertEquals(self.parser.strip_quotes("'foo'"), "foo")
    
    def test_002_unquote2(self):
        """parser.ScssImportsParser: unquote case 2"""
        self.assertEquals(self.parser.strip_quotes('"foo"'), "foo")
    
    def test_003_unquote3(self):
        """parser.ScssImportsParser: unquote case 3"""
        self.assertEquals(self.parser.strip_quotes("foo"), "foo")
    
    def test_004_unquote4(self):
        """parser.ScssImportsParser: unquote case 4"""
        self.assertEquals(self.parser.strip_quotes("'foo"), "'foo")
    
    
    def test_010_remove_comment(self):
        """parser.ScssImportsParser: removing singleline comment case 1"""
        self.assertEquals(self.parser.remove_comments("""// foo"""), "")
    
    def test_011_remove_comment(self):
        """parser.ScssImportsParser: removing singleline comment case 2"""
        self.assertEquals(self.parser.remove_comments("""//foo
            """).strip(), "")
    
    def test_012_remove_comment(self):
        """parser.ScssImportsParser: removing singleline comment case 3"""
        self.assertEquals(self.parser.remove_comments("""
            //foo
        """).strip(), "")
    
    def test_013_remove_comment(self):
        """parser.ScssImportsParser: removing singleline comment case 4"""
        self.assertEquals(self.parser.remove_comments("""$foo: true;
            // foo
            $bar: false;
            """).strip(), """$foo: true;\n                        $bar: false;""")
    
    def test_015_remove_comment(self):
        """parser.ScssImportsParser: removing multiline comment case 1"""
        self.assertEquals(self.parser.remove_comments("""/* foo */"""), "")
    
    def test_016_remove_comment(self):
        """parser.ScssImportsParser: removing multiline comment case 2"""
        self.assertEquals(self.parser.remove_comments("""
            /* 
             * foo
             */""").strip(), "")
    
    def test_017_remove_comment(self):
        """parser.ScssImportsParser: removing multiline comment case 3"""
        self.assertEquals(self.parser.remove_comments("""
            /* 
             * foo
             */
             $bar: true;""").strip(), "$bar: true;")
    
    def test_018_remove_comment(self):
        """parser.ScssImportsParser: removing singleline and multiline comments"""
        self.assertEquals(self.parser.remove_comments("""//Start
/* 
 * Pika
 */
$foo: true;
// Boo
$bar: false;
// End""").strip(), "$foo: true;\n$bar: false;")
    
    
    def test_020_flatten_rules1(self):
        """parser.ScssImportsParser: flatten_rules case 1"""
        rules = self.parser.flatten_rules([
            ('', '"foo"'),
        ])
        self.assertEquals(rules, [
            'foo',
        ])
    
    def test_021_flatten_rules2(self):
        """parser.ScssImportsParser: flatten_rules case 2"""
        rules = self.parser.flatten_rules([
            ('', "'bar'"),
        ])
        self.assertEquals(rules, [
            'bar',
        ])
    
    def test_022_flatten_rules3(self):
        """parser.ScssImportsParser: flatten_rules case 3"""
        rules = self.parser.flatten_rules([
            ('', "'bar'"),
            ('url', '"wrong"'),
            ('', '"cool", "plop"'),
            ('', '"wrong.css"'),
            ('', '"https://wrong"'),
        ])
        self.assertEquals(rules, [
            'bar',
            'cool', 'plop',
        ])
    
    
    def test_100_basic(self):
        """parser.ScssImportsParser: basic file"""
        with open(os.path.join(self.fixtures_dir, 'basic_project/main_basic.scss')) as fp:
            result = self.parser.parse(fp.read())
        self.dummy_output(result)
        self.assertEquals(result, [
            'vendor', 'utils/mixins', 'sass_filetest', 'css_filetest', '_empty',
            'components/filename_test_1', 'components/_filename_test_2',
            'components/filename_test_3.scss',
            'components/_filename_test_4.scss',
            'components/filename_test_5.plop',
            'components/filename_test_6.plop.scss',
            'components/../empty',
        ])
    
    def test_101_empty(self):
        """parser.ScssImportsParser: empty file"""
        with open(os.path.join(self.fixtures_dir, 'basic_project/_empty.scss')) as fp:
            result = self.parser.parse(fp.read())
        self.dummy_output(result)
        self.assertEquals(result, [])
    
    def test_102_noimport(self):
        """parser.ScssImportsParser: no import rules"""
        with open(os.path.join(self.fixtures_dir, 'basic_project/_vendor.scss')) as fp:
            result = self.parser.parse(fp.read())
        self.dummy_output(result)
        self.assertEquals(result, [])
    
    def test_103_comment1(self):
        """parser.ScssImportsParser: commented import 1 (buggy behavior)"""
        result = self.parser.parse("""//@import "compass/css3";""")
        self.assertEquals(result, [])
    
    def test_104_comment2(self):
        """parser.ScssImportsParser: commented import 2 (buggy behavior)"""
        result = self.parser.parse("""//      @import "compass/css3";""")
        self.assertEquals(result, [])
    
    def test_105_comment3(self):
        """parser.ScssImportsParser: commented import 3 (buggy behavior)"""
        result = self.parser.parse("""/*
            @import "compass/css3";
            */""")
        self.assertEquals(result, [])



class case_02_ResolverTestCase(unittest.TestCase):
    """Unittest to resolve import paths"""
    
    def setUp(self):
        self.debug = False
        self.parser = ScssImportsParser()
        self.resolver = ImportPathsResolver()
        self.fixtures_dir = os.path.join(os.path.abspath(os.path.dirname(boussole.__file__)), 'test_fixtures')
    
    def dummy_output(self, content):
        # Just output something to print for debugguing
        if self.debug:
            print content
    
    def test_001_candidate_basic(self):
        """resolver.ImportPathsResolver: Underscore leading and candidate extensions"""
        self.assertEquals(self.resolver.candidate_paths("foo"), [
            "foo.scss",
            "_foo.scss",
            "foo.sass",
            "_foo.sass",
            "foo.css",
            "_foo.css",
        ])
    
    def test_002_extension_uncandidate(self):
        """resolver.ImportPathsResolver: Uncandidate extension"""
        self.assertEquals(self.resolver.candidate_paths("foo.plop"), [
            "foo.plop.scss",
            "_foo.plop.scss",
            "foo.plop.sass",
            "_foo.plop.sass",
            "foo.plop.css",
            "_foo.plop.css",
        ])
    
    def test_003_candidate_extension_ready(self):
        """resolver.ImportPathsResolver: Candidate extension allready in place"""
        self.assertEquals(self.resolver.candidate_paths("foo.scss"), [
            "foo.scss",
            "_foo.scss",
        ])
    
    def test_004_candidate_complex1(self):
        """resolver.ImportPathsResolver: Complex case 1 for candidates"""
        self.assertEquals(self.resolver.candidate_paths("components/addons/foo.plop.scss"), [
            "components/addons/foo.plop.scss",
            "components/addons/_foo.plop.scss",
        ])
    
    def test_005_candidate_complex2(self):
        """resolver.ImportPathsResolver: Complex case 2 for candidates"""
        self.assertEquals(self.resolver.candidate_paths("../components/../addons/foo.plop"), [
            "../components/../addons/foo.plop.scss",
            "../components/../addons/_foo.plop.scss",
            "../components/../addons/foo.plop.sass",
            "../components/../addons/_foo.plop.sass",
            "../components/../addons/foo.plop.css",
            "../components/../addons/_foo.plop.css",
        ])
    
    
    def test_010_check_candidate_ok1(self):
        """resolver.ImportPathsResolver: Check candidates correct case 1"""
        basepath = os.path.join(self.fixtures_dir, "basic_project")
        candidates = self.resolver.candidate_paths("vendor")
        self.assertEquals(
            self.resolver.check_candidate_exists(basepath, candidates),
            os.path.join(basepath, "_vendor.scss"))
    
    def test_011_check_candidate_ok2(self):
        """resolver.ImportPathsResolver: Check candidates correct case 2"""
        basepath = os.path.join(self.fixtures_dir, "basic_project")
        candidates = self.resolver.candidate_paths("components/_filename_test_2")
        self.assertEquals(
            self.resolver.check_candidate_exists(basepath, candidates),
            os.path.join(basepath, "components/_filename_test_2.scss"))
    
    def test_012_check_candidate_ok3(self):
        """resolver.ImportPathsResolver: Check candidates correct case 3"""
        basepath = os.path.join(self.fixtures_dir, "basic_project")
        candidates = self.resolver.candidate_paths("components/filename_test_6.plop.scss")
        self.assertEquals(
            self.resolver.check_candidate_exists(basepath, candidates),
            os.path.join(basepath, "components/_filename_test_6.plop.scss"))
    
    def test_013_check_candidate_ok4(self):
        """resolver.ImportPathsResolver: Check candidates correct case 4"""
        basepath = os.path.join(self.fixtures_dir, "basic_project", "components")
        candidates = self.resolver.candidate_paths("webfont")
        self.assertEquals(
            self.resolver.check_candidate_exists(basepath, candidates),
            os.path.join(basepath, "_webfont.scss"))
    
    def test_014_check_candidate_ok5(self):
        """resolver.ImportPathsResolver: Check candidates correct case 5"""
        basepath = os.path.join(self.fixtures_dir, "basic_project", "components")
        candidates = self.resolver.candidate_paths("../components/webfont_icons")
        self.assertEquals(
            self.resolver.check_candidate_exists(basepath, candidates),
            os.path.join(basepath, "../components/_webfont_icons.scss"))
    
    def test_015_check_candidate_wrong1(self):
        """resolver.ImportPathsResolver: Check candidates wrong case 1"""
        basepath = os.path.join(self.fixtures_dir, "basic_project")
        candidates = self.resolver.candidate_paths("dont_exists")
        self.assertEquals(self.resolver.check_candidate_exists(basepath, candidates), False)
    
    def test_016_check_candidate_wrong2(self):
        """resolver.ImportPathsResolver: Check candidates wrong case 2"""
        basepath = os.path.join(self.fixtures_dir, "basic_project")
        candidates = self.resolver.candidate_paths("css_filetest.sass")
        self.assertEquals(self.resolver.check_candidate_exists(basepath, candidates), False)
    
    def test_100_check_library1(self):
        """resolver.ImportPathsResolver: Resolve paths from main_using_libs.scss that use included libraries"""
        basepath = os.path.join(self.fixtures_dir, "basic_project")
        sourcepath = os.path.join(basepath, 'main_using_libs.scss')
        lib1path = os.path.join(self.fixtures_dir, 'library_1')
        lib2path = os.path.join(self.fixtures_dir, 'library_2')
        with open(sourcepath) as fp:
            finded_paths = self.parser.parse(fp.read())
        resolved_paths = self.resolver.resolve(sourcepath, finded_paths, library_paths=[lib1path, lib2path])
        self.assertEquals(resolved_paths, [
            os.path.join(lib2path, 'addons/_some_addon.scss'),
            os.path.join(basepath, 'main_basic.scss'),
            os.path.join(basepath, 'components/_webfont.scss'),
            os.path.join(lib1path, 'library_1_fullstack.scss'),
        ])


if __name__ == "__main__":
    unittest.main()
