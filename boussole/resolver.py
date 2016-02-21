# -*- coding: utf-8 -*-
"""
Resolver

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

TODO: LIBRARY PATHS FOR FUCKIN SANITY!
"""
import os

class InvalidImportRule(Exception):
    pass


class ImportPathsResolver(object):
    """
    Import paths resolver
    
    NOTE: think about import libs, current position is primary choices then 
    import libs can be matched against (does import libs order does matter?)
    """
    # Order does matter
    CANDIDATE_EXTENSIONS = ['scss', 'sass', 'css', ]
    STRICT_PATH_VALIDATION = True
    
    def sanitize_path(self, path):
        """
        Allways return an absolute path, with expanded home user (if any) and 
        normalized path
        """
        path = os.path.expanduser(path)
        if not os.path.isabs(path):
            path = os.path.abspath(fixture_filepath)
        path = os.path.normpath(path)
        return path

    def candidate_paths(self, filepath):
        """
        Return candidates path for given path
        
        * Three available extensions (scss, sass, css);
        * Filename can be prefixed or not with '_' character;
        """
        filelead, filetail = os.path.split(filepath)
        name, extension = os.path.splitext(filetail)
        # Removed leading dot from extension
        if extension:
            extension = extension[1:]
        #print "<filelead:{}> <name:{}> <extension:{}>".format(filelead, name, extension)
        
        filenames = [name]
        # If underscore prefix is present, dont need to double underscore
        if not name.startswith('_'):
            filenames.append("_{}".format(name))
        
        # If explicit extension, dont need to add more candidate extensions
        if extension and extension in self.CANDIDATE_EXTENSIONS:
            filenames = [".".join([k, extension]) for k in filenames]
        # Else if no extension or not candidate, add candidate extensions
        else:
            # Restore uncandidate extensions if any
            if extension:
                filenames = [".".join([k, extension]) for k in filenames]
            new = []
            for ext in self.CANDIDATE_EXTENSIONS:
                new.extend([".".join([k, ext]) for k in filenames])
            filenames = new
        
        #print "filenames:", filenames
        # Return candidates with restored leading path if any
        return [os.path.join(filelead, v) for v in filenames]
    
    def check_candidate_exists(self, basepath, candidates):
        """
        Check that at least one candidate exist into basepath
        
        Return False if don't exists, else return the elected candidate
        """
        for item in candidates:
            abspath = os.path.join(basepath, item)
            if os.path.exists(abspath):
                return item
            
        return False
    
    def resolve(self, sourcepath, paths, library_paths=None):
        """
        Resolve given paths from the given source path
        
        TODO: ..and from given library paths
        
        Return resolved path list.
        
        * Raise exception 'InvalidImportRule' if a path does not exist and 
          ImportPathsResolver.STRICT_PATH_VALIDATION is True, else just 
          drop the path;
        * If path exists, add it to the resolved path list;
        
        
        Note: libsass resolve imported path only from the current main file 
        path position, never from the relative project position. Meaning that 
        a file ``a/foo.scss`` cannot import something like 
        ``@import "a/bar.scss"``, it must do instead ``@import "bar.scss"``.
        Then if not finded, it can try to resolve from imported library root 
        position.
        """
        basepath, filename = os.path.split(sourcepath)
        resolved_paths = []
        
        #print "SOURCEPATH:", sourcepath
        #print "BASEPATH:", basepath
        #print
        
        for import_rule in paths:
            #print "* @import:", import_rule
            candidates = self.candidate_paths(import_rule)
            existing = self.check_candidate_exists(basepath, candidates)
            if existing:
                #print "   -", existing
                resolved_paths.append(existing)
                
            # TODO: This would be instead a check in library_paths, some fake 
            # libs have to be added in fixtures before
            elif self.STRICT_PATH_VALIDATION:
                raise InvalidImportRule("Imported path '{}' does not exist in '{}'".format(import_rule, basepath))
        
        return resolved_paths


# For some development debug
if __name__ == "__main__":
    import boussole
    from boussole.parser import ScssImportsParser
    
    
    def test(filepath):
        parser = ScssImportsParser()
        
        with open(filepath) as fp:
            print "Opening:", filepath
            finded_paths = parser.parse(fp.read())
        print
        
        print "Finded paths:"
        for k in finded_paths:
            print "-", k
        print
        
        resolver = ImportPathsResolver()
        resolved_paths = resolver.resolve(filepath, finded_paths)
        print "Resolved paths:"
        for k in resolved_paths:
            print "-", k
        print
    
    
    boussole_dir = os.path.dirname(boussole.__file__)
    fixtures_dir = os.path.join(os.path.abspath(boussole_dir), 'test_fixtures')
    
    fixture_path = os.path.join(fixtures_dir, 'basic_project/main_basic.scss')
    test(fixture_path)
    
    #print 
    #print "#"*80
    #fixture_path = os.path.join(fixtures_dir, 'basic_project/main_error.scss')
    #test(fixture_path)
    
    