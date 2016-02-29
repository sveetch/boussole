# -*- coding: utf-8 -*-
"""
Unittests
"""
import os, unittest

import boussole
from boussole.parser import ScssImportsParser
from boussole.resolver import InvalidImportRule, ImportPathsResolver
from boussole.inspector import ScssInspector


class FixturesSettingsTestMixin(unittest.TestCase):
    """Unittest mixin containing some basic settings"""
    def setUp(self):
        self.debug = False
        
        # Base fixture datas directory
        self.fixtures_dir = 'test_fixtures'
        self.fixtures_path = os.path.join(os.path.abspath(os.path.dirname(boussole.__file__)), self.fixtures_dir)
        
        # Sample project
        self.sample_dir = "sample_project"
        self.sample_path = os.path.join(self.fixtures_path, self.sample_dir)
        
        # Some sample libraries
        self.lib1_dir = 'library_1'
        self.lib2_dir = 'library_2'
        self.lib1_path = os.path.join(self.fixtures_path, self.lib1_dir)
        self.lib2_path = os.path.join(self.fixtures_path, self.lib2_dir)
        self.libraries_fixture_paths = [
            self.lib1_path,
            self.lib2_path,
        ]
    
    def dummy_output(self, content):
        # Just output something to print for debugguing
        if self.debug:
            print content

class ParserTestMixin(FixturesSettingsTestMixin):
    """Unittest mixin for parser"""
    def setUp(self):
        super(ParserTestMixin, self).setUp()
        
        self.parser = ScssImportsParser()

class ResolverTestMixin(ParserTestMixin):
    """Unittest mixin for resolver"""
    def setUp(self):
        super(ResolverTestMixin, self).setUp()
        
        self.resolver = ImportPathsResolver()

class InspectorTestMixin(FixturesSettingsTestMixin):
    """Unittest mixin for inspector"""
    def setUp(self):
        super(InspectorTestMixin, self).setUp()
        
        self.inspector = ScssInspector()



class case_01_ParserQuotesTestCase(ParserTestMixin):
    """Unittests for parser: Unquotes"""
    def test_parser_001_unquote1(self):
        """parser.ScssImportsParser: unquote case 1"""
        self.assertEquals(self.parser.strip_quotes("'foo'"), "foo")
    
    def test_parser_002_unquote2(self):
        """parser.ScssImportsParser: unquote case 2"""
        self.assertEquals(self.parser.strip_quotes('"foo"'), "foo")
    
    def test_parser_003_unquote3(self):
        """parser.ScssImportsParser: unquote case 3"""
        self.assertEquals(self.parser.strip_quotes("foo"), "foo")
    
    def test_parser_004_unquote4(self):
        """parser.ScssImportsParser: unquote case 4"""
        self.assertEquals(self.parser.strip_quotes("'foo"), "'foo")



class case_02_ParserCommentsTestCase(ParserTestMixin):
    """Unittests for parser: Removing comments"""
    def test_parser_010_remove_comment(self):
        """parser.ScssImportsParser: removing singleline comment case 1"""
        self.assertEquals(self.parser.remove_comments("""// foo"""), "")
    
    def test_parser_011_remove_comment(self):
        """parser.ScssImportsParser: removing singleline comment case 2"""
        self.assertEquals(self.parser.remove_comments("""//foo
            """).strip(), "")
    
    def test_parser_012_remove_comment(self):
        """parser.ScssImportsParser: removing singleline comment case 3"""
        self.assertEquals(self.parser.remove_comments("""
            //foo
        """).strip(), "")
    
    def test_parser_013_remove_comment(self):
        """parser.ScssImportsParser: removing singleline comment case 4"""
        self.assertEquals(self.parser.remove_comments("""$foo: true;
// foo
$bar: false;
""").strip(), """$foo: true;\n$bar: false;""")
    
    def test_parser_014_remove_comment(self):
        """parser.ScssImportsParser: removing singleline comment case 5"""
        self.assertEquals(self.parser.remove_comments("""@import "vendor"; //foo""").strip(), """@import "vendor";""")
    
    def test_parser_015_remove_comment(self):
        """parser.ScssImportsParser: removing multiline comment case 1"""
        self.assertEquals(self.parser.remove_comments("""/* foo */"""), "")
    
    def test_parser_016_remove_comment(self):
        """parser.ScssImportsParser: removing multiline comment case 2"""
        self.assertEquals(self.parser.remove_comments("""
            /* 
             * foo
             */""").strip(), "")
    
    def test_parser_017_remove_comment(self):
        """parser.ScssImportsParser: removing multiline comment case 3"""
        self.assertEquals(self.parser.remove_comments("""
            /* 
             * foo
             */
             $bar: true;""").strip(), "$bar: true;")
    
    def test_parser_018_remove_comment(self):
        """parser.ScssImportsParser: removing singleline and multiline comments"""
        self.assertEquals(self.parser.remove_comments("""//Start
/* 
 * Pika
 */
$foo: true;
// Boo
$bar: false;
// End""").strip(), "$foo: true;\n$bar: false;")



class case_03_ParserFlattenTestCase(ParserTestMixin):
    """Unittests for parser: Flatten import rules"""
    def test_parser_020_flatten_rules1(self):
        """parser.ScssImportsParser: flatten_rules case 1"""
        rules = self.parser.flatten_rules([
            ('', '"foo"'),
        ])
        self.assertEquals(rules, [
            'foo',
        ])
    
    def test_parser_021_flatten_rules2(self):
        """parser.ScssImportsParser: flatten_rules case 2"""
        rules = self.parser.flatten_rules([
            ('', "'bar'"),
        ])
        self.assertEquals(rules, [
            'bar',
        ])
    
    def test_parser_022_flatten_rules3(self):
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



class case_04_ParserParseTestCase(ParserTestMixin):
    """Unittests for parser: Parsing source for import rules (rely on FS)"""
    def test_parser_001_parse_comment1(self):
        """parser.ScssImportsParser: commented import 1 (buggy behavior)"""
        result = self.parser.parse("""//@import "compass/css3";""")
        self.assertEquals(result, [])
    
    def test_parser_002_parse_comment2(self):
        """parser.ScssImportsParser: commented import 2 (buggy behavior)"""
        result = self.parser.parse("""//      @import "compass/css3";""")
        self.assertEquals(result, [])
    
    def test_parser_003_parse_comment3(self):
        """parser.ScssImportsParser: commented import 3 (buggy behavior)"""
        result = self.parser.parse("""/*
            @import "compass/css3";
            */""")
        self.assertEquals(result, [])
        
    def test_parser_100_parse_sample(self):
        """parser.ScssImportsParser: complete file"""
        with open(os.path.join(self.fixtures_path, self.sample_dir, 'main_full.scss')) as fp:
            result = self.parser.parse(fp.read())
        self.assertEquals(result, [
            'vendor', 'utils/mixins', 'sass_filetest', 'css_filetest', '_empty',
            'components/filename_test_1', 'components/_filename_test_2',
            'components/filename_test_3.scss',
            'components/_filename_test_4.scss',
            'components/filename_test_5.plop',
            'components/filename_test_6.plop.scss',
            'components/../empty',
        ])
    
    def test_parser_101_parse_empty(self):
        """parser.ScssImportsParser: empty file"""
        with open(os.path.join(self.fixtures_path, self.sample_dir, '_empty.scss')) as fp:
            result = self.parser.parse(fp.read())
        self.assertEquals(result, [])
    
    def test_parser_102_parse_noimport(self):
        """parser.ScssImportsParser: no import rules"""
        with open(os.path.join(self.fixtures_path, self.sample_dir, '_vendor.scss')) as fp:
            result = self.parser.parse(fp.read())
        self.assertEquals(result, [])



class case_10_ResolverCandidatesTestCase(ResolverTestMixin):
    """Unittests for resolver: Candidate files"""
    
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



class case_11_ResolverCheckingTestCase(ResolverTestMixin):
    """Unittests for resolver: Checking candidates (rely on FS)"""
    
    def test_010_check_candidate_ok1(self):
        """resolver.ImportPathsResolver: Check candidates correct case 1"""
        candidates = self.resolver.candidate_paths("vendor")
        self.assertEquals(
            self.resolver.check_candidate_exists(self.sample_path, candidates),
            os.path.join(self.sample_path, "_vendor.scss"))
    
    def test_011_check_candidate_ok2(self):
        """resolver.ImportPathsResolver: Check candidates correct case 2"""
        candidates = self.resolver.candidate_paths("components/_filename_test_2")
        self.assertEquals(
            self.resolver.check_candidate_exists(self.sample_path, candidates),
            os.path.join(self.sample_path, "components/_filename_test_2.scss"))
    
    def test_012_check_candidate_ok3(self):
        """resolver.ImportPathsResolver: Check candidates correct case 3"""
        candidates = self.resolver.candidate_paths("components/filename_test_6.plop.scss")
        self.assertEquals(
            self.resolver.check_candidate_exists(self.sample_path, candidates),
            os.path.join(self.sample_path, "components/_filename_test_6.plop.scss"))
    
    def test_013_check_candidate_ok4(self):
        """resolver.ImportPathsResolver: Check candidates correct case 4"""
        basepath = os.path.join(self.sample_path, "components")
        candidates = self.resolver.candidate_paths("webfont")
        self.assertEquals(
            self.resolver.check_candidate_exists(basepath, candidates),
            os.path.join(basepath, "_webfont.scss"))
    
    def test_014_check_candidate_ok5(self):
        """resolver.ImportPathsResolver: Check candidates correct case 5"""
        basepath = os.path.join(self.sample_path, "components")
        candidates = self.resolver.candidate_paths("../components/webfont_icons")
        self.assertEquals(
            self.resolver.check_candidate_exists(basepath, candidates),
            os.path.join(basepath, "../components/_webfont_icons.scss"))
    
    def test_015_check_candidate_wrong1(self):
        """resolver.ImportPathsResolver: Check candidates wrong case 1"""
        candidates = self.resolver.candidate_paths("dont_exists")
        self.assertEquals(self.resolver.check_candidate_exists(self.sample_path, candidates), False)
    
    def test_016_check_candidate_wrong2(self):
        """resolver.ImportPathsResolver: Check candidates wrong case 2"""
        candidates = self.resolver.candidate_paths("css_filetest.sass")
        self.assertEquals(self.resolver.check_candidate_exists(self.sample_path, candidates), False)



class case_12_ResolverResolvingTestCase(ResolverTestMixin):
    """Unittests for resolver: Resolving import paths from a source (rely on FS)"""
    
    def test_100_check_basic(self):
        """resolver.ImportPathsResolver: Resolve paths from basic sample"""
        sourcepath = os.path.join(self.sample_path, 'main_basic.scss')
        with open(sourcepath) as fp:
            finded_paths = self.parser.parse(fp.read())
        resolved_paths = self.resolver.resolve(sourcepath, finded_paths)
        self.assertEquals(resolved_paths, [
            os.path.join(self.sample_path, '_vendor.scss'),
            os.path.join(self.sample_path, '_empty.scss'),
        ])
    
    def test_101_check_library(self):
        """resolver.ImportPathsResolver: Resolve paths from main_using_libs.scss that use included libraries"""
        sourcepath = os.path.join(self.sample_path, 'main_using_libs.scss')
        with open(sourcepath) as fp:
            finded_paths = self.parser.parse(fp.read())
        resolved_paths = self.resolver.resolve(sourcepath, finded_paths, library_paths=self.libraries_fixture_paths)
        self.assertEquals(resolved_paths, [
            os.path.join(self.lib2_path, 'addons/_some_addon.scss'),
            os.path.join(self.sample_path, 'main_basic.scss'),
            os.path.join(self.sample_path, 'components/_webfont.scss'),
            os.path.join(self.lib1_path, 'library_1_fullstack.scss'),
        ])
    
    def test_103_check_commented(self):
        """resolver.ImportPathsResolver: Resolve paths from sample with comments"""
        sourcepath = os.path.join(self.sample_path, 'main_commented.scss')
        with open(sourcepath) as fp:
            finded_paths = self.parser.parse(fp.read())
        resolved_paths = self.resolver.resolve(sourcepath, finded_paths)
        self.assertEquals(resolved_paths, [
            os.path.join(self.sample_path, '_vendor.scss'),
            os.path.join(self.sample_path, 'components/_filename_test_1.scss'),
            os.path.join(self.sample_path, '_empty.scss'),
        ])
    
    def test_110_check_error(self):
        """resolver.ImportPathsResolver: Exception on wrong import path"""
        sourcepath = os.path.join(self.sample_path, 'main_error.scss')
        with open(sourcepath) as fp:
            finded_paths = self.parser.parse(fp.read())
        self.assertRaises(InvalidImportRule, self.resolver.resolve, sourcepath,
                          finded_paths, 
                          library_paths=self.libraries_fixture_paths)



class case_20_InspectorTestCase(InspectorTestMixin):
    """Unittests for inspector: Retrieving dependancies from a sources (rely on FS)"""
    
    def tearDown(self):
        """Reset inspector memory after each test"""
        self.inspector.reset()
    
    def test_inspector_001_basic(self):
        """inspector.ScssInspector: Dependancies of basic sample"""
        sourcepath = os.path.join(self.sample_path, 'main_basic.scss')
        self.inspector.inspect(sourcepath)
        self.assertEquals(list(self.inspector.dependancies(sourcepath)), [
            os.path.join(self.sample_path, '_vendor.scss'), 
            os.path.join(self.sample_path, '_empty.scss'),
        ])
    


if __name__ == "__main__":
    unittest.main()
