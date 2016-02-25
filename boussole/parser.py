# -*- coding: utf-8 -*-
"""
SCSS parser

SASS Reference about "@import" rule:

    http://sass-lang.com/documentation/file.SASS_REFERENCE.html#import
"""
import re

class ScssImportsParser(object):
    """
    A modest SCSS parser that is just able to find import rules
    
    Sass syntax (also known as "indented syntax") is not supported, 
    import rules is different (not quoted and don't finish on 
    semi-colon ";", just a newline), so current regex can't match them. It 
    would need another dedicated regex to parse them.
    """
    # TODO: Regex is buggy, it does not honor comments // or /*..*/ so 
    # commented imports are matched too..  Solutions:
    # 1. Find a perfect regex, this not seems possible;
    # 2. Code a "Finite-state machine" parser;
    # 3. Pre process content using regexes to remove all comments;
    REGEX_IMPORT_RULE = re.compile(ur'@import\s*(url)?\s*\(?([^;]+?)\)?;', 
                                   re.IGNORECASE)
    REGEX_COMMENTS = re.compile(r'(/\*.*?\*/)|(//.*?(\n|$))', 
                                         re.IGNORECASE | re.DOTALL)

    def strip_quotes(self, content):
        """
        Naive quote stripping because regex return them in results (sic..)
        """
        if (content.startswith('"') and content.endswith('"')) or \
           (content.startswith("'") and content.endswith("'")):
            return content[1:-1]
        
        return content
    
    def remove_comments(self, content):
        """
        Remove all comment kind (inline and multiline)
        """
        return self.REGEX_COMMENTS.sub("", content)
    
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
        # Remove all comments before searching for import rules, to not catch 
        # commented breaked import rules
        declarations = self.REGEX_IMPORT_RULE.findall(
            self.remove_comments(content)
        )
        return self.flatten_rules(declarations)


# For some development debug
if __name__ == "__main__":
    import os
    import boussole
    
    fixtures = os.path.join(
        os.path.abspath(os.path.dirname(boussole.__file__)),
        'test_fixtures')
    
    parser = ScssImportsParser()
    
    with open(os.path.join(fixtures, 'basic_project/main_basic.scss')) as fp:
        finded_paths = parser.parse(fp.read())
    print finded_paths
    