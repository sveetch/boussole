# -*- coding: utf-8 -*-
"""
SCSS parser

SASS Reference about "@import" rule:

    http://sass-lang.com/documentation/file.SASS_REFERENCE.html#import
"""
import os, re

class ScssImportsParser(object):
    """
    A modest SCSS parser that is just able to find import rules
    
    Sass syntax (also known as "indented syntax") is not supported (yet?), 
    import rules is different: they are not quoted and don't finish on 
    semi-colon ";", so the current regex can't match them. It would need an 
    dedicated regex to use on some extension (sass/scss) detect.
    """
    REGEX_IMPORT_RULE = re.compile(ur'@import\s*(url)?\s*\(?([^;]+?)\)?;', 
                                   re.IGNORECASE)
    
    def strip_quotes(self, content):
        """
        Naive quote stripping because regex return them in results (sic..)
        """
        if (content.startswith('"') and content.endswith('"')) or \
           (content.startswith("'") and content.endswith("'")):
            return content[1:-1]
        
        return content
    
    def flatten_rules(self, declarations):
        """
        Flatten returned rules from regex because import rules on multiple 
        line are not cleanly parsed as distinct matchs
        """
        rules = []
        
        for protocole,paths in declarations:
            #print protocole, ",",paths
            # If there is a protocole (like 'url), drop it
            if protocole:
                continue
            # Unquote and possibly split multiple rule in the same declaration
            rules.extend( [self.strip_quotes(v.strip()) 
                           for v in paths.split(',')] )
        
        # Lambda to filter items that:
        # * Starts with http:// or https:// (this for external load only)
        # * Ends with ".css" (they are not intended to be compiled)
        drop_unprocessed = lambda x: not(x.startswith('http://') or \
                            x.startswith('https://') or x.endswith('.css'))
            
        return filter(drop_unprocessed, rules)
    
    def parse(self, content):
        """
        Parse a stylesheet document with a regex to extract all import rules 
        and return them
        """
        declarations = self.REGEX_IMPORT_RULE.findall(content)    
        return self.flatten_rules(declarations)


# For some development debug
if __name__ == "__main__":
    import boussole
    
    fixtures = os.path.join(
        os.path.abspath(os.path.dirname(boussole.__file__)),
        'test_fixtures')
    
    parser = ScssImportsParser()
    
    with open(os.path.join(fixtures, 'basic_project/main_basic.scss')) as fp:
        finded_paths = parser.parse(fp.read())
    print finded_paths