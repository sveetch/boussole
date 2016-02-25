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
"""
import os, re

from boussole.parser import ScssImportsParser
from boussole.resolver import ImportPathsResolver

class ScssInspector(ImportPathsResolver, ScssImportsParser):
    """
    SCSS file inspector for import paths
    """
    _PATHS_MAP = {}
    NOT_INSPECTED_EXTENSIONS = ['css', 'sass']
    
    def look_source(self, sourcepath, library_paths=None):
        """
        Open a SCSS file (sourcepath) and find all involved file through 
        imports
        """
        with open(sourcepath) as fp:
            print "Opening:", sourcepath
            finded_paths = self.parse(fp.read())
        print
        
        resolved_paths = self.resolve(sourcepath, finded_paths, 
                                      library_paths=library_paths)
        
        self._PATHS_MAP[sourcepath] = resolved_paths
        
        # Start recursive finding through each resolved path that has not been 
        # collected yet
        for path in resolved_paths:
            if path not in self._PATHS_MAP:
                self.look_source(path, library_paths=library_paths)
        
        return
    
    def inspect(self, sourcepath, library_paths=None):
        """
        Recursively retrieve all imported paths from a given SCSS file
        """
        # Reboot map for each full inspect
        self._PATHS_MAP = {}
        
        # Start from the source then recursively walk into imports to populate 
        # the map
        self.look_source(sourcepath, library_paths=library_paths)
        
        return self._PATHS_MAP


# For some development debug
if __name__ == "__main__":
    import boussole
    import json
    
    boussole_dir = os.path.dirname(boussole.__file__)
    fixtures_dir = os.path.join(os.path.abspath(boussole_dir), 'test_fixtures')
    fixture_path = os.path.join(fixtures_dir, 'basic_project/main_using_libs.scss')
    library1_path = os.path.join(fixtures_dir, 'library_1/')
    library2_path = os.path.join(fixtures_dir, 'library_2/')
    
    inspector = ScssInspector()
    
    results = inspector.inspect(fixture_path, library_paths=[library1_path, library2_path])
    
    print json.dumps(results, indent=4)
