# -*- coding: utf-8 -*-
"""
Unittests
"""
import os, unittest

from boussole.parser import ScssImportsParser

class case_01_ParserTestCase(unittest.TestCase):
    """Unittest to parse import rules"""
    
    def setUp(self):
        self.debug = False
        self.parser = ScssImportsParser()
        self.fixtures_paths = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test_fixtures')
    
    def dummy_output(self, content):
        # Just output something to print for debugguing
        if self.debug:
            print content
    
    def test_010_basic(self):
        """parser.ScssImportsParser: basic file"""
        with open(os.path.join(self.fixtures_paths, 'basic_project/main_basic.scss')) as fp:
            result = self.parser.parse(fp.read())
        self.dummy_output(result)
        self.assertEquals(result, [
            'vendor', 'utils/mixins', 'sass_filetest', 'css_filetest', 'empty',
            'components/filename_test_1', 'components/_filename_test_2',
            'components/filename_test_3.scss',
            'components/_filename_test_4.scss'
        ])
    
    def test_011_empty(self):
        """parser.ScssImportsParser: empty file"""
        with open(os.path.join(self.fixtures_paths, 'basic_project/_empty.scss')) as fp:
            result = self.parser.parse(fp.read())
        self.dummy_output(result)
        self.assertEquals(result, [])
    
    def test_012_noimport(self):
        """parser.ScssImportsParser: no import rules"""
        with open(os.path.join(self.fixtures_paths, 'basic_project/_vendor.scss')) as fp:
            result = self.parser.parse(fp.read())
        self.dummy_output(result)
        self.assertEquals(result, [])


if __name__ == "__main__":
    unittest.main()
