# -*- coding: utf-8 -*-
"""
Validators

Name resolving cases: ::

    //For Real filename: "components/_header.scss"
    @import "components/header"; //OK
    @import "components/_header"; //OK
    @import "components/header.scss"; //OK
    @import "components/_header.scss"; //OK

If two files has multiple resolutions cases, this leads to an error: ::

    sassc: error: Error: It's not clear which file to import for '@import "main_basic"'.
        Candidates:
            main_basic.scss
            main_basic.css
        Please delete or rename all but one of these files.
            on line 6 of main_with_subimports.scss
    >> @import "main_basic";
    ^

"""
import os

class InvalidImportRule(Exception):
    pass


class ImportPathsValidator(object):
    """
    Import paths validator
    
    Note: think about import libs, current position is primary choices then 
    import libs can be matched against (does import libs order does matter?)
    """
    def validate(self, filepath, paths):
        """
        Validate that given paths exists from filepath position
        """
        return 


# For some development debug
if __name__ == "__main__":
    fixtures_paths = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test_fixtures')
    parser = ScssImportsParser()
    with open(os.path.join(fixtures_paths, 'basic_project/main_basic.scss')) as fp:
        result = parser.parse(fp.read())
    print result