# -*- coding: utf-8 -*-
"""
Inspector

We need:

* [DONE] To collect every imported files into a map (where key is the source 
  and contain a list of imported paths);
* To have another map or object to be able to find all imports involved for 
  a file;
* To collect every files that are "partials" files (not starting with "_"): 
  they are intended to be compiled through sass when one of their import 
  (recursively) is triggered (change, del, etc..);

Last one may be in another mixin/interface as it involves source dir and FS 
usage.

Note: Does Compass trigger compile when there is changes on some library_paths files ?

Some thinking
=============

Simple case
-----------

* Inspector detect change on app.scss
  -> Trigger compilation of app.scss

REVERSE_DEPENDANCIES = {
    'app.scss': []
}


Depth case
----------

* Inspector detect changes on components/webfont.scss
    + webfont.scss file is directly used by minimal.scss
    + components/webfont.scss file is directly used by addons/foo.scss
        - addons/foo.scss file is directly used by app.scss
  -> Trigger compilation of app.scss then minimal.scss

REVERSE_DEPENDANCIES = {
    'components/webfont.scss': [
        'addons/foo.scss',
        'minimal.scss',
        'app.scss',
    ]
    'addons/foo.scss': [
        'app.scss',
    ]
}

"""
import os, re
from collections import defaultdict

from boussole.parser import ScssImportsParser
from boussole.resolver import ImportPathsResolver

class ScssInspector(ImportPathsResolver, ScssImportsParser):
    """
    SCSS file inspector for import paths
    """
    NOT_INSPECTED_EXTENSIONS = ['css', 'sass']
    
    def __init__(self, *args, **kwargs):
        self.reset()
    
    def look_source(self, sourcepath, library_paths=None):
        """
        Open a SCSS file (sourcepath) and find all involved file through 
        imports
        """
        with open(sourcepath) as fp:
            print "Opening:", sourcepath
            finded_paths = self.parse(fp.read())
        
        resolved_paths = self.resolve(sourcepath, finded_paths, 
                                      library_paths=library_paths)
        
        self._PATHS_MAP[sourcepath] = resolved_paths
        
        for p in resolved_paths:
            self._DEPENDANCIES[p].add(sourcepath)
        
        # Start recursive finding through each resolved path that has not been 
        # collected yet
        for path in resolved_paths:
            if path not in self._PATHS_MAP:
                self.look_source(path, library_paths=library_paths)
        
        return
    
    def reset(self):
        """
        Reset maps
        """
        self._PATHS_MAP = {}
        self._DEPENDANCIES = defaultdict(set)
    
    def inspect(self, *args, **kwargs):
        """
        Recursively retrieve all imported paths from all given SCSS files
        """
        library_paths = kwargs.get('library_paths', None)
        
        for sourcepath in args:
            self.look_source(sourcepath, library_paths=library_paths)
        
        return self._PATHS_MAP
    
    def dependancies(self, sourcepath):
        """
        Return dependancies from a source
        """
        # Direct dependancies
        print "Searching dependancies for:", sourcepath
        print
        deps = set([])
        deps.update(self._PATHS_MAP.get(sourcepath, []))
        
        # Recursive search starting from direct deps
        for item in deps.copy():
            deps.update(self.dependancies(item))
        
        return deps
    
    def reverse(self, sourcepath):
        """
        Return reverse dependancies from a source
        """
        # Direct dependancies
        print "Searching reverse dependancies for:", sourcepath
        print
        deps = set([])
        deps.update(self._DEPENDANCIES.get(sourcepath, []))
        
        # Recursive search starting from direct deps
        for item in deps.copy():
            deps.update(self.reverse(item))
        
        return deps


# For some development debug
if __name__ == "__main__":
    import boussole
    import json
    
    def shortpath(path, base_dir):
        if path.startswith(base_dir):
            return path[len(base_dir):]
        return path
    
    def shortenize_paths(paths_map, base_dir):
        new_map = {}
        for k,v in paths_map.items():
            new_map[shortpath(k, base_dir)] = [shortpath(item, base_dir) for item in v]
        return new_map
    
    boussole_dir = os.path.dirname(boussole.__file__)
    fixtures_dir = os.path.join(os.path.abspath(boussole_dir), 'test_fixtures')
    library1_path = os.path.join(fixtures_dir, 'library_1/')
    library2_path = os.path.join(fixtures_dir, 'library_2/')
    
    inspector = ScssInspector()
    
    sources = [
        os.path.join(fixtures_dir, 'sample_project/main_full.scss'),
        os.path.join(fixtures_dir, 'sample_project/main_commented.scss'),
        os.path.join(fixtures_dir, 'sample_project/main_basic.scss'),
        os.path.join(fixtures_dir, 'sample_project/main_with_subimports.scss'),
        os.path.join(fixtures_dir, 'sample_project/main_using_libs.scss'),
        os.path.join(fixtures_dir, 'sample_project/main_circular_1.scss'),
        os.path.join(fixtures_dir, 'sample_project/main_circular_2.scss'),
    ]
    
    results_full = inspector.inspect(*sources, library_paths=[library1_path, library2_path])
    
    #print json.dumps(results_basic, indent=4)
    #print
    #print "#"*100
    #print
    
    print json.dumps(shortenize_paths(inspector._PATHS_MAP, fixtures_dir), indent=4)
    print
    print "#"*100
    print
    
    #print json.dumps(shortenize_paths(inspector._DEPENDANCIES, fixtures_dir), indent=4)
    #print
    #print "#"*100
    #print
    
    print json.dumps(
        list(
            inspector.dependancies(os.path.join(fixtures_dir, 'sample_project/main_using_libs.scss'))
        ),
        indent=4
    )
    print
    print "#"*100
    print
    
    #print json.dumps(
        #list(
            #inspector.reverse(os.path.join(fixtures_dir, 'sample_project/components/_webfont_icons.scss'))
        #),
        #indent=4
    #)
    #print
    #print "#"*100
    #print
