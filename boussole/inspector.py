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

NOTE: Does Compass trigger compile when there is changes on some library_paths files ?

"""
from collections import defaultdict

from boussole.exceptions import CircularImport
from boussole.parser import ScssImportsParser
from boussole.resolver import ImportPathsResolver

class CatchedRuntimeError(CircularImport):
    pass

# Temp during debug
import json
def shortpath(path, base_dir):
    if path.startswith(base_dir):
        return path[len(base_dir):]
    return path

def shorten_paths_map(paths_map, base_dir):
    new_map = {}
    for k,v in paths_map.items():
        new_map[shortpath(k, base_dir)] = [shortpath(item, base_dir) for item in v]
    return new_map

def shorten_paths_list(paths_list, base_dir):
    return [shortpath(k, base_dir) for k in paths_list]



class ScssInspector(ImportPathsResolver, ScssImportsParser):
    """
    SCSS file inspector for import paths
    """
    NOT_INSPECTED_EXTENSIONS = ['css', 'sass']
    
    def __init__(self, *args, **kwargs):
        self.reset()
    
    def reset(self):
        """
        Reset internal maps
        """
        self._CHILDREN_MAP = {}
        self._PARENTS_MAP = defaultdict(set)
    
    def look_source(self, sourcepath, library_paths=None):
        """
        Open a SCSS file (sourcepath) and find all involved file through 
        imports
        """
        # Don't inspect again source that has allready be inspected as a 
        # children of a previous source. Is it the right behavior ?
        if sourcepath not in self._CHILDREN_MAP:
            with open(sourcepath) as fp:
                finded_paths = self.parse(fp.read())
            
            children = self.resolve(sourcepath, finded_paths, 
                                        library_paths=library_paths)
            
            # Those files that are imported by the sourcepath
            self._CHILDREN_MAP[sourcepath] = children
            
            # Those files that import the sourcepath
            for p in children:
                self._PARENTS_MAP[p].add(sourcepath)
            
            # Start recursive finding through each resolved path that has not been 
            # collected yet
            for path in children:
                if path not in self._CHILDREN_MAP:
                    self.look_source(path, library_paths=library_paths)
        
            
        return
    
    def inspect(self, *args, **kwargs):
        """
        Recursively inspect all given SCSS files to find import children 
        and parents
        """
        library_paths = kwargs.get('library_paths', None)
        
        for sourcepath in args:
            self.look_source(sourcepath, library_paths=library_paths)
        
        return self._CHILDREN_MAP
    
    def _old_children_implement(self, sourcepath, recursive=True):
        """
        Return children imported by file from given source path
        
        NOTE: Keeped until new implement has been strongly validated/tested
        """
        # Direct dependencies
        deps = set([])
        deps.update(self._CHILDREN_MAP.get(sourcepath, []))
        
        # Recursive search starting from direct deps
        if recursive:
            for item in deps.copy():
                if item in self._PARENTS_MAP[sourcepath]:
                    msg = "A circular import has been detected between '{}' "\
                           "and '{}'"
                    raise CircularImport(msg.format(sourcepath, item))
                try:
                    deps.update(self._old_children_implement(item))
                except RuntimeError:
                    msg = "A circular import has occured by '{}'"
                    raise CatchedRuntimeError(msg.format(item))
        
        return deps
    
    def _old_parents_implement(self, sourcepath, recursive=True):
        """
        Return parents that import the given source path
        
        NOTE: Keeped until new implement has been strongly validated/tested
        """
        # Direct dependencies
        deps = set([])
        deps.update(self._PARENTS_MAP.get(sourcepath, []))
        
        # Recursive search starting from direct deps
        if recursive:
            for item in deps.copy():
                if item in self._CHILDREN_MAP[sourcepath]:
                    msg = "A circular import has been detected between '{}' "\
                            "and '{}'"
                    raise CircularImport(msg.format(sourcepath, item))
                try:
                    deps.update(self.parents(item))
                except RuntimeError:
                    msg = "A circular import has occured by '{}'"
                    raise CatchedRuntimeError(msg.format(item))
        
        return deps
    
    def children(self, sourcepath, recursive=True):
        """
        Return children imported by file from given source path
        """
        base_dir = '/home/emencia/projects/sass_addons/boussole/tests/data_fixtures/sample_project/'
        
        title = "Kids are working on '{}'".format(shortpath(sourcepath, base_dir=base_dir))
        print
        print "."*len(title)
        print title
        print "."*len(title)
        print
        
        return self._get_recursive_dependancies(self._CHILDREN_MAP, sourcepath, recursive=True)
    
    def parents(self, sourcepath, recursive=True):
        """
        Return parents that import the given source path
        """
        base_dir = '/home/emencia/projects/sass_addons/boussole/tests/data_fixtures/sample_project/'
        
        title = "Parents are sleeping on '{}'".format(shortpath(sourcepath, base_dir=base_dir))
        print
        print "."*len(title)
        print title
        print "."*len(title)
        print
        
        return self._get_recursive_dependancies(self._PARENTS_MAP, sourcepath, recursive=True)
    
    def _get_recursive_dependancies(self, dependencies_map, sourcepath, recursive=True):
        """
        Return all dependencies of a source, recursively searching through its dependencies
        """
        base_dir = '/home/emencia/projects/sass_addons/boussole/tests/data_fixtures/sample_project/'
        
        # Direct dependencies
        collected = set([])
        collected.update(dependencies_map.get(sourcepath, []))
        print "~> Direct source deps are:", shorten_paths_list(collected, base_dir=base_dir)
        
        sequence = collected.copy() # Sequence of source to explore
        walkthrough = [] # Exploration list
        
        # Recursive search starting from direct dependencies
        if recursive:
            while True:
                if not sequence:
                    print "/!\ Deps are empty, nothing to do, bye"
                    break
                item = sequence.pop()
                
                print
                print "* Item:", shortpath(item, base_dir=base_dir)
                # Add current source to the explorated source list
                walkthrough.append(item)
                
                # Current item children
                current_item_dependancies = dependencies_map.get(item, [])
                print "  - Current item dependancies:", shorten_paths_list(current_item_dependancies, base_dir=base_dir)
                
                for dependency in current_item_dependancies:
                    # Allready visited item, ignore and continue to the new item
                    if dependency in walkthrough:
                        print "    - Allready visited:", shortpath(dependency, base_dir=base_dir)
                        continue
                    # Unvisited item yet, add its children to dependencies and item to explore
                    else:
                        print "    - Will visit:", shortpath(dependency, base_dir=base_dir)
                        collected.add(dependency)
                        sequence.add(dependency)
                
                # Sourcepath has allready been visited but present itself again, assume it's a circular import
                if sourcepath in walkthrough:
                    print
                    print "(!) CircularImport exception to be raised, stopping loop operations (!)"
                    print
                    msg = "A circular import has occured by '{}'"
                    raise CircularImport(msg.format(current_item_dependancies))
                
                # No more item to explore, break loop
                if not sequence:
                    break
        
        print
        print "=> Walked through:", shorten_paths_list(shorten_paths_list(walkthrough, base_dir=base_dir), base_dir=base_dir)
        print "."*200
        
        return collected


# For some development debug
if __name__ == "__main__":
    import os, json
    import boussole
    
    #def shortpath(path, base_dir):
        #if path.startswith(base_dir):
            #return path[len(base_dir):]
        #return path
    
    #def shorten_paths_map(paths_map, base_dir):
        #new_map = {}
        #for k,v in paths_map.items():
            #new_map[shortpath(k, base_dir)] = [shortpath(item, base_dir) for item in v]
        #return new_map
    
    #def shorten_paths_list(paths_list, base_dir):
        #return [shortpath(k, base_dir) for k in paths_list]
    
    class ComplexEncoder(json.JSONEncoder):
        """
        Allow to encode properly some objet types
        """
        def default(self, obj):
            if isinstance(obj, set):
                return list(obj)
            return json.JSONEncoder.default(self, obj)
    
    boussole_dir = os.path.dirname(boussole.__file__)
    fixtures_dir = os.path.normpath(os.path.join(os.path.abspath(boussole_dir), '..', 'tests', 'data_fixtures'))
    sample_path = os.path.join(fixtures_dir, 'sample_project')
    library1_path = os.path.join(fixtures_dir, 'library_1')
    library2_path = os.path.join(fixtures_dir, 'library_2')
    library_paths = [library1_path, library2_path]
    
    inspector = ScssInspector()
    
    sources = [
        os.path.join(sample_path, 'main_basic.scss'),
        os.path.join(sample_path, 'main_syntax.scss'),
        os.path.join(sample_path, 'main_commented.scss'),
        os.path.join(sample_path, 'main_depth_import-1.scss'),
        os.path.join(sample_path, 'main_depth_import-2.scss'),
        os.path.join(sample_path, 'main_depth_import-3.scss'),
        os.path.join(sample_path, 'main_with_subimports.scss'),
        os.path.join(sample_path, 'main_using_libs.scss'),
        os.path.join(sample_path, 'main_circular_0.scss'),
        os.path.join(sample_path, 'main_circular_1.scss'),
        os.path.join(sample_path, 'main_circular_2.scss'),
        os.path.join(sample_path, 'main_circular_3.scss'),
        os.path.join(sample_path, 'main_circular_4.scss'),
        os.path.join(sample_path, 'main_circular_bridge.scss'),
        os.path.join(sample_path, 'main_circular_5.scss'),
    ]
    
    basic_sourcepath = os.path.join(sample_path, 'main_basic.scss')
    depth1_sourcepath = os.path.join(sample_path, 'main_depth_import-1.scss')
    depth2_sourcepath = os.path.join(sample_path, 'main_depth_import-2.scss')
    depth3_sourcepath = os.path.join(sample_path, 'main_depth_import-3.scss')
    subimports_sourcepath = os.path.join(sample_path, 'main_with_subimports.scss')
    usinglibs_sourcepath = os.path.join(sample_path, 'main_using_libs.scss')
    circular0_sourcepath = os.path.join(sample_path, 'main_circular_0.scss')
    circular1_sourcepath = os.path.join(sample_path, 'main_circular_1.scss')
    circular2_sourcepath = os.path.join(sample_path, 'main_circular_2.scss')
    circular3_sourcepath = os.path.join(sample_path, 'main_circular_3.scss')
    circular4_sourcepath = os.path.join(sample_path, 'main_circular_4.scss')
    circularbridge_sourcepath = os.path.join(sample_path, 'main_circular_bridge.scss')
    circular5_sourcepath = os.path.join(sample_path, 'main_circular_5.scss')
    
    results = inspector.inspect(*sources, library_paths=library_paths)
    
    # Display maps from inspection
    print "-"*80
    print "Sources that import other sources (_CHILDREN_MAP)"
    print "-"*80
    
    print json.dumps(shorten_paths_map(inspector._CHILDREN_MAP, sample_path+'/'), indent=4)
    print
    
    
    print
    print "-"*80
    print "Sources that are imported by other sources (_PARENTS_MAP)"
    print "-"*80
    
    print json.dumps(shorten_paths_map(inspector._PARENTS_MAP, sample_path+'/'), indent=4, cls=ComplexEncoder)
    print
    
    print "~"*200
    
    def display_oldchildren_process(sourcepath):
        print
        print "-"*80
        print "(inspector._old_children_implement) They are imported by:", shortpath(sourcepath, sample_path+'/')
        print "-"*80
        
        try:
            deps = list(inspector._old_children_implement(sourcepath))
        except CatchedRuntimeError:
            print "[!] CatchedRuntimeError error has been raised [!]"
        except CircularImport:
            print "[!] CircularImport error has been raised [!]"
        else:
            
            print json.dumps(shorten_paths_list(deps, sample_path+'/'), indent=4)
            print
    
    
    def display_children_process(sourcepath):
        print
        print "-"*80
        print "(inspector.children) They are imported by:", shortpath(sourcepath, sample_path+'/')
        print "-"*80
        
        try:
            deps = list(inspector.children(sourcepath))
        except CatchedRuntimeError:
            print "[!] CatchedRuntimeError error has been raised [!]"
        except CircularImport:
            print "[!] CircularImport error has been raised [!]"
        else:
            print json.dumps(shorten_paths_list(deps, sample_path+'/'), indent=4)
            print
    
    
    # Basic sample
    display_oldchildren_process(basic_sourcepath)
    display_children_process(basic_sourcepath)
    
    print "~"*200
    
    # Depth sample
    display_oldchildren_process(depth3_sourcepath)
    display_children_process(depth3_sourcepath)
    
    print "~"*200
    
    # 
    display_oldchildren_process(usinglibs_sourcepath)
    display_children_process(usinglibs_sourcepath)
    
    print "~"*200
    
    # Some test for case 1>2
    display_oldchildren_process(circular1_sourcepath)
    display_children_process(circular1_sourcepath)
    
    print "~"*200
    
    # Some test for case 3>bridge>4
    display_oldchildren_process(circular3_sourcepath)
    display_children_process(circular3_sourcepath)
    
    print "~"*200
    
    # Final case for sub circular import
    display_oldchildren_process(circular5_sourcepath)
    display_children_process(circular5_sourcepath)
    
    print "~"*200
    
    # Self circular import
    display_oldchildren_process(circular0_sourcepath)
    display_children_process(circular0_sourcepath)
    
    
    
    
    
    
    #revs = list(inspector.parents(circular3_sourcepath))
    
    #print
    #print "-"*80
    #print "(inspector.parents) They import source:", circular3_sourcepath
    #print "-"*80
    
    #print json.dumps(revs, indent=4)
    #print
    
    
    ## Display dependencies from a source
    #deps = list(inspector._old_children_implement(circular4_sourcepath))
    
    #revs = list(inspector.parents(circular4_sourcepath))
    
    #print
    #print "-"*80
    #print "(inspector._old_children_implement) They are imported by:", circular4_sourcepath
    #print "-"*80
    
    #print json.dumps(deps, indent=4)
    #print
    
    #print
    #print "-"*80
    #print "(inspector.parents) They import source:", circular4_sourcepath
    #print "-"*80
    
    #print json.dumps(revs, indent=4)
    #print
