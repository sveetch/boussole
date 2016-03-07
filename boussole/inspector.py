# -*- coding: utf-8 -*-
"""
Inspector
=========

.. todo::
    Does Compass trigger compile when there is changes on some library_paths
    files ?

.. todo::
    Identical path resolving for different file: ::

        sassc: error: Error:
            It's not clear which file to import for '@import "main_basic"'.
            Candidates:
                main_basic.scss
                main_basic.css
"""
from collections import defaultdict

from boussole.exceptions import CircularImport
from boussole.parser import ScssImportsParser
from boussole.resolver import ImportPathsResolver


class ScssInspector(ImportPathsResolver, ScssImportsParser):
    """
    Project inspector for SCSS sources

    Inspect sources to search for their dependencies.

    ``__init__`` method use ``reset`` method to initialize some internal
    buffers.

    Attributes:
        _CHILDREN_MAP: Dictionnary of finded direct children for each
            inspected sources.
        _PARENTS_MAP: Dictionnary of finded direct parents for each inspected
            sources.
        NOT_INSPECTED_EXTENSIONS: List of file extensions to ignore for
            path inspection.
    """
    NOT_INSPECTED_EXTENSIONS = ['css', 'sass']

    def __init__(self, *args, **kwargs):
        self.reset()

    def reset(self):
        """
        Reset internal buffers ``_CHILDREN_MAP`` and ``_PARENTS_MAP``.
        """
        self._CHILDREN_MAP = {}
        self._PARENTS_MAP = defaultdict(set)

    def _get_recursive_dependancies(self, dependencies_map, sourcepath,
                                    recursive=True):
        """
        Return all dependencies of a source, recursively searching through its
        dependencies.

        This is a common method used by ``children`` and ``parents`` methods.

        Args:
            dependencies_map (dict): Internal buffer (internal buffers
                ``_CHILDREN_MAP`` or ``_PARENTS_MAP``) to use for searching.
            sourcepath (str): Source file path to start searching for
                dependencies.

        Keyword Arguments:
            recursive (bool): Switch to enabled recursive finding (if True).
                Default to True.

        Returns:
            set: List of dependencies paths.
        """
        # Direct dependencies
        collected = set([])
        collected.update(dependencies_map.get(sourcepath, []))

        # Sequence of source to explore
        sequence = collected.copy()
        # Exploration list
        walkthrough = []

        # Recursive search starting from direct dependencies
        if recursive:
            while True:
                if not sequence:
                    break
                item = sequence.pop()

                # Add current source to the explorated source list
                walkthrough.append(item)

                # Current item children
                current_item_dependancies = dependencies_map.get(item, [])

                for dependency in current_item_dependancies:
                    # Allready visited item, ignore and continue to the new
                    # item
                    if dependency in walkthrough:
                        continue
                    # Unvisited item yet, add its children to dependencies and
                    # item to explore
                    else:
                        collected.add(dependency)
                        sequence.add(dependency)

                # Sourcepath has allready been visited but present itself
                # again, assume it's a circular import
                if sourcepath in walkthrough:
                    msg = "A circular import has occured by '{}'"
                    raise CircularImport(msg.format(current_item_dependancies))

                # No more item to explore, break loop
                if not sequence:
                    break

        return collected

    def look_source(self, sourcepath, library_paths=None):
        """
        Open a SCSS file (sourcepath) and find all involved file through
        imports.

        This will fill internal buffers ``_CHILDREN_MAP`` and ``_PARENTS_MAP``.

        Args:
            sourcepath (str): Source file path to start searching for imports.

        Keyword Arguments:
            library_paths (list): List of directory paths for libraries to
                resolve paths if resolving fails on the base source path.
                Default to None.
        """
        # Don't inspect again source that has allready be inspected as a
        # children of a previous source
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

            # Start recursive finding through each resolved path that has not
            # been collected yet
            for path in children:
                if path not in self._CHILDREN_MAP:
                    self.look_source(path, library_paths=library_paths)

        return

    def inspect(self, *args, **kwargs):
        """
        Recursively inspect all given SCSS files to find import children
        and parents.

        This does not return anything. Just fill internal buffers about
        inspected files.

        Note:
            This will ignore orphan files (files that are not imported from
            any of given SCSS files).

        Args:
            *args: One or multiple arguments, each one for a source file path
                to inspect.

        Keyword Arguments:
            library_paths (list): List of directory paths for libraries to
                resolve paths if resolving fails on the base source path.
                Default to None.
        """
        library_paths = kwargs.get('library_paths', None)

        for sourcepath in args:
            self.look_source(sourcepath, library_paths=library_paths)

    def children(self, sourcepath, recursive=True):
        """
        Recursively find all children that are imported from the given source
        path.

        Args:
            sourcepath (str): Source file path to search for.

        Keyword Arguments:
            recursive (bool): Switch to enabled recursive finding (if True).
                Default to True.

        Returns:
            set: List of finded parents path.
        """
        return self._get_recursive_dependancies(self._CHILDREN_MAP, sourcepath,
                                                recursive=True)

    def parents(self, sourcepath, recursive=True):
        """
        Recursively find all parents that import the given source path.

        Args:
            sourcepath (str): Source file path to search for.

        Keyword Arguments:
            recursive (bool): Switch to enabled recursive finding (if True).
                Default to True.

        Returns:
            set: List of finded parents path.
        """
        return self._get_recursive_dependancies(self._PARENTS_MAP, sourcepath,
                                                recursive=True)
