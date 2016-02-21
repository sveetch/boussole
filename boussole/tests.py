# -*- coding: utf-8 -*-
"""
Unittests
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
        """parser.ScssImportsParser: unquote test 1"""
        self.assertEquals(self.parser.strip_quotes("'foo'"), "foo")
    
    def test_002_unquote2(self):
        """parser.ScssImportsParser: unquote test 2"""
        self.assertEquals(self.parser.strip_quotes('"foo"'), "foo")
    
    def test_003_unquote3(self):
        """parser.ScssImportsParser: unquote test 3"""
        self.assertEquals(self.parser.strip_quotes("foo"), "foo")
    
    def test_004_unquote4(self):
        """parser.ScssImportsParser: unquote test 4"""
        self.assertEquals(self.parser.strip_quotes("'foo"), "'foo")
    
    
    def test_010_flatten_rules1(self):
        """parser.ScssImportsParser: flatten_rules test 1"""
        rules = self.parser.flatten_rules([
            ('', '"foo"'),
        ])
        self.assertEquals(rules, [
            'foo',
        ])
    
    def test_011_flatten_rules2(self):
        """parser.ScssImportsParser: flatten_rules test 2"""
        rules = self.parser.flatten_rules([
            ('', "'bar'"),
        ])
        self.assertEquals(rules, [
            'bar',
        ])
    
    def test_012_flatten_rules3(self):
        """parser.ScssImportsParser: flatten_rules test 3"""
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
        self.assertEquals(self.resolver.check_candidate_exists(basepath, candidates), "_vendor.scss")
    
    def test_011_check_candidate_ok2(self):
        """resolver.ImportPathsResolver: Check candidates correct case 2"""
        basepath = os.path.join(self.fixtures_dir, "basic_project")
        candidates = self.resolver.candidate_paths("components/_filename_test_2")
        self.assertEquals(self.resolver.check_candidate_exists(basepath, candidates), "components/_filename_test_2.scss")
    
    def test_012_check_candidate_ok3(self):
        """resolver.ImportPathsResolver: Check candidates correct case 3"""
        basepath = os.path.join(self.fixtures_dir, "basic_project")
        candidates = self.resolver.candidate_paths("components/filename_test_6.plop.scss")
        self.assertEquals(self.resolver.check_candidate_exists(basepath, candidates), "components/_filename_test_6.plop.scss")
    
    def test_013_check_candidate_ok4(self):
        """resolver.ImportPathsResolver: Check candidates correct case 4"""
        basepath = os.path.join(self.fixtures_dir, "basic_project", "components")
        candidates = self.resolver.candidate_paths("webfont")
        self.assertEquals(self.resolver.check_candidate_exists(basepath, candidates), "_webfont.scss")
    
    def test_014_check_candidate_ok5(self):
        """resolver.ImportPathsResolver: Check candidates correct case 5"""
        basepath = os.path.join(self.fixtures_dir, "basic_project", "components")
        candidates = self.resolver.candidate_paths("../components/webfont_icons")
        self.assertEquals(self.resolver.check_candidate_exists(basepath, candidates), "../components/_webfont_icons.scss")
    
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
        sourcepath = os.path.join(self.fixtures_dir, 'basic_project/main_using_libs.scss')
        lib1path = os.path.join(self.fixtures_dir, 'library_1')
        lib2path = os.path.join(self.fixtures_dir, 'library_2')
        with open(sourcepath) as fp:
            finded_paths = self.parser.parse(fp.read())
        resolved_paths = self.resolver.resolve(sourcepath, finded_paths, library_paths=[lib1path, lib2path])
        self.assertEquals(resolved_paths, [
            'addons/_some_addon.scss',
            'main_basic.scss',
            'components/_webfont.scss',
            'library_1_fullstack.scss',
        ])


if __name__ == "__main__":
    unittest.main()
