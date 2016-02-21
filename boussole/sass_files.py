# -*- coding: utf-8 -*-
"""
SaSS files management

Old handmade script, deprecated
"""
import os, re

class InvalidImportRule(Exception):
    pass

class ProjectScanner(object):
    """
    Recursively walk through a directory and correct every finded path within 
    '@import' rule to a path relative to the library root (given as instance argument)
    """
    REGEX_IMPORT_RULE = re.compile(ur'@import\s*(url)?\s*\(?([^;]+?)\)?;', re.IGNORECASE)
    project_map = {}
    
    def __init__(self, sources_dir, included_paths):
        self.sources_dir = sources_dir
        self.included_paths = included_paths
    
    def strip_quotes(self, content):
        """
        Naive quote stripping
        """
        if not content.startswith('"') and not content.startswith("'"):
            return content
        
        return content[1:-1]

    def build_possibilites(self, lead, tail, ext):
        return [
            os.path.join(lead, "{}.{}".format(tail, ext)),
            os.path.join(lead, "_{}.{}".format(tail, ext)),
        ]
    
    def get_name_variants(self, lead, tail):
        """
        Return a list of all filename possibilities:
        
        * Three available extensions (scss, sass, css);
        * Filename can be prefixed or not with '_' character;
        """
        clean_ext = lambda x: '.'.join(tail.split('.')[:-1])
        if tail.endswith('.scss'):
            possibilities = self.build_possibilites(lead, clean_ext(tail), 'scss')
        
        elif tail.endswith('.sass'):
            tail = tail.split('.')[:-1]
            possibilities = self.build_possibilites(lead, clean_ext(tail), 'sass')
        
        elif tail.endswith('.css'):
            tail = tail.split('.')[:-1]
            possibilities = self.build_possibilites(lead, clean_ext(tail), 'css')
            
        else:
            possibilities = self.build_possibilites(lead, tail, 'scss')
            possibilities += self.build_possibilites(lead, tail, 'sass')
            possibilities += self.build_possibilites(lead, tail, 'css')
            
        return possibilities

    def search_file_path(self, path):
        """
        Try to find accurate path for given import rule
        
        Path resolving is the following:
        
        1. Search for file relative to current file;
        2. If not finded search for file relative to library root;
        
        Each file searching is done on various filename possibility in order:
        
        1. FILENAME.scss
        2. _FILENAME.scss
        3. FILENAME.sass
        4. _FILENAME.sass
        
        As soon as a file is finded, it's returned and stop further search.
        """
        lead, tail = os.path.split(path)
        
        name_variants = self.get_name_variants(lead, tail)
        
        # Possible paths for current relative position (starts from the current file)
        local_name_variants = [os.path.realpath(os.path.join(self._current_path, p)) for p in name_variants]
        
        # Possible paths for absolute relative position (starts from the library root)
        absolute_name_variants = [os.path.realpath(os.path.join(self.sources_dir, p)) for p in name_variants]
        
        # Return the first valid path
        for var in local_name_variants+absolute_name_variants:
            if os.path.exists(var):
                return os.path.relpath(var, self.sources_dir)
                
        return None
    


    def search_import_rules(self, path, filename):
        """
        Import rules search using a (not so bad) regex
        """
        filepath = os.path.join(path, filename)
        
        # Find all rules in file
        with open(filepath, 'rb') as fp:
            content = fp.read()
            declarations = self.REGEX_IMPORT_RULE.findall(content)
        
        # All rules on same declaration line
        paths = []
        for declaration in declarations:
            # Split multiple rule in the same declaration and unquote them
            rules = [self.strip_quotes(v.strip()) for v in declaration[1].split(',')]
            
            for item in rules:
                print "   * Original:", item
                path = self.search_file_path(item)
                
                paths.append("{}".format(path or ''))
                if path:
                    print "     - ", path
                else:
                    print "     - Unable to find any valid path"
            
        return paths
    
    
    
    def rule_replacer(self, matchobj):
        """
        Path each path in @import declaration
        """
        declarations = matchobj.groups()
        
        # Dont modify 'url' kind
        if declarations[0] == 'url':
            return u"@import url({});".format(declarations[1])
        elif self.strip_quotes(declarations[1]).startswith('http://') or self.strip_quotes(declarations[1]).startswith('https://'):
            return u"@import {};".format(', '.join(declarations[1:]))
        
        # All rules on same declaration line
        paths = []
        for declaration in declarations[1:]:
            # Split multiple rule in the same declaration and unquote them
            rules = [self.strip_quotes(v.strip()) for v in declaration.split(',')]
            
            for item in rules:
                #print "   * Original:", item
                path = self.search_file_path(item)
                head, tail = os.path.split(path)
                # Remove '_' if any (TODO: should not be performed on other than sass/scss)
                if tail.startswith('_'):
                    path = os.path.join(head, tail[1:])
                #print "path:", path
                if not path:
                    raise InvalidImportRule(u'Unable to find file for path "{source}" in "{filepath}"'.format(source=item, filepath=self._current_file))
                else:
                    # Remove extension for sass files
                    root, ext = os.path.splitext(path)
                    if ext in ('.scss', '.sass'):
                        paths.append("'{}'".format(root))
                    else:
                        paths.append("'{}'".format(path))
        
        return u"@import {};".format(', '.join(paths))

    def patch_import_rules(self, path, filename):
        """
        Patch import rules
        """
        filepath = os.path.join(path, filename)
        
        # Find all rules in file
        with open(filepath, 'rb') as fp:
            content = fp.read()
            declarations = self.REGEX_IMPORT_RULE.findall(content)
        
        result = self.REGEX_IMPORT_RULE.sub(self.rule_replacer, content)
        #print result
        
        with open(filepath, 'wb') as fp:
            content = fp.write(result)



    def scan(self):
        """
        Walk source directory to scan and map for @import rules in every sass/scss files
        """
        self.project_map = {}
        
        for root, dirs, files in os.walk(self.sources_dir):
            self._current_path = root
            self._current_dir = os.path.relpath(self._current_path, self.sources_dir)
            if self._current_dir == '.':
                self._current_dir = ''
                
            print u"========= {} =========".format(self._current_path)
            print u"   [Relative dir: '{}']".format(self._current_dir)
            print
            
            #i = 0
            for filename in files:
            #for filename in ['foundation_toast.scss']:
                if filename.endswith('.scss') or filename.endswith('.sass'):
                    print u"@ SOURCE FILE: {}".format(filename)
                    self._current_file = filename
                    self.search_import_rules(self._current_path, filename)            
                    #self.patch_import_rules(self._current_path, filename)            
                    print
                
                ## Temp breakpoint to avoid too much debug output
                #i += 1
                #if i >= 1:
                    #break
            print
            #break


# Very basic usage during development
PROJECT_PATH = "../../demo/sources/sass/scss/"
INCLUDE_PATHS = (
    'demo/sources/sass/foundation5/',
    'demo/sources/sass/bourbon/',
)
if os.path.exists(PROJECT_PATH):
    cleaner = ProjectScanner(PROJECT_PATH, included_paths=INCLUDE_PATHS)
    cleaner.scan()
else:
    print "Given path does not exists:", PROJECT_PATH
