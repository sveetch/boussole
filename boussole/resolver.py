# -*- coding: utf-8 -*-
"""
Resolvers
=========

.. _SASS @import Reference:
    http://sass-lang.com/documentation/file.SASS_REFERENCE.html#import

.. _SASS partials Reference:
    http://sass-lang.com/documentation/file.SASS_REFERENCE.html#partials

"""
import os

from boussole.exceptions import UnresolvablePath

class ImportPathsResolver(object):
    """
    Import paths resolver.
    
    Resolve given paths from SCSS source to absolute paths.

    Example:
        These rules will be resolved: ::

            // Real filename: "components/_header.scss"
            @import "components/header";
            @import "components/_header";
            @import "components/header.scss";
            @import "components/_header.scss";
    
    It's a mixin, meaning without own ``__init__`` method so it's should be 
    safe enough to inherit it from another class.

    Attributes:
        CANDIDATE_EXTENSIONS (list): List of extensions available to build 
            candidate paths. Beware, order does matter, the first extension 
            will be the top candidate.
        STRICT_PATH_VALIDATION (bool): A switch to enabled (``True``) or 
            disable (``False``) exception raising when a path can not be 
            resolved.
    """
    CANDIDATE_EXTENSIONS = ['scss', 'sass', 'css', ]
    STRICT_PATH_VALIDATION = True
    
    def candidate_paths(self, filepath):
        """
        Return candidates path for given path
        
        * If Filename does not starts with ``_``, will build a candidate for 
          both with and without ``_`` prefix;
        * Will build For each available extensions if filename does not have 
          an explicit extension;
        * Leading path directory is preserved;
        
        Args:
            filepath (str): Relative path as finded in an import rule from a 
                SCSS source.

        Returns:
            list: Builded candidate paths (as relative paths).
        """
        filelead, filetail = os.path.split(filepath)
        name, extension = os.path.splitext(filetail)
        # Removed leading dot from extension
        if extension:
            extension = extension[1:]
        
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
        
        # Return candidates with restored leading path if any
        return [os.path.join(filelead, v) for v in filenames]
    
    def check_candidate_exists(self, basepath, candidates):
        """
        Check that at least one candidate exist into a directory.
        
        Args:
            basepath (str): Directory path where to search for candidate.
            candidates (list): List of candidate file paths.

        Returns:
            ``False`` if no candidate exists else return the elected path.
        """
        for item in candidates:
            abspath = os.path.join(basepath, item)
            if os.path.exists(abspath):
                return abspath
            
        return False
    
    def resolve(self, sourcepath, paths, library_paths=None):
        """
        Resolve given paths from given base paths
        
        Return resolved path list.
        
        Note: 
            Resolving strategy is made like libsass do, meaning paths in 
            import rules is resolved from the source where the import rules 
            have been finded.
        
        Args:
            sourcepath (str): Source file path, its directory is used to 
                resolve given paths. The path must be an absolute path to 
                avoid errors on resolving.
            paths (list): Relative paths (from ``sourcepath``) to resolve.
            library_paths (list): List of directory paths for libraries to 
                resolve paths if resolving fails on the base source path.
                Default to None.

        Raises:
            UnresolvablePath: If a path does not exist and 
                ``STRICT_PATH_VALIDATION`` attribute is ``True``.

        Returns:
            list: List of resolved path.
        """
        # Split basedir/filename from sourcepath, so the first resolving 
        # basepath is the sourcepath directory, then the optionnal 
        # given libraries
        basedir, filename = os.path.split(sourcepath)
        basepaths = [basedir]
        resolved_paths = []
        
        # Add given library paths to the basepaths for resolving
        # Accept a string if not allready in basepaths
        if library_paths and isinstance(library_paths, basestring) and \
            library_paths not in basepaths:
            basepaths.append(library_paths)
        # Add path item from list if not allready in basepaths
        elif library_paths:
            for k in list(library_paths):
                if k not in basepaths:
                    basepaths.append(k)
        
        for import_rule in paths:
            candidates = self.candidate_paths(import_rule)
            
            existing = False
            # The first resolved candidate from basepaths wins
            for i,basepath in enumerate(basepaths):
                existing = self.check_candidate_exists(basepath, candidates)
                if existing:
                    # Normalized resolved path
                    resolved_paths.append(os.path.normpath(existing))
                    break

            if not existing and self.STRICT_PATH_VALIDATION:
                raise UnresolvablePath(
                    "Imported path '{}' does not exist in '{}'".format(
                        import_rule, basedir
                    )
                )
        
        return resolved_paths
