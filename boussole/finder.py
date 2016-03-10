# -*- coding: utf-8 -*-
"""
Finder
======
"""
import os


class ScssFinder(object):
    """
    Project finder for SCSS sources

    Attributes:
        FINDER_COMPILABLE_EXTS: List of file extensions regarded as compilable
            sources.
    """
    FINDER_COMPILABLE_EXTS = ['scss', 'sass']

    def get_compilable_sources(self, paths, recursive=True):
        """
        Find all scss sources that should be compiled, aka all sources that
        are not "partials" SASS sources.

        This is a common method used by ``children`` and ``parents`` methods.

        Args:
            paths (list): Directory paths to scan.

        Keyword Arguments:
            recursive (bool): Switch to enabled recursive finding (if True).
                Default to True.

        Returns:
            set: List of source paths.

        """
        filepaths = []

        for sourcedir in paths:
            for root, dirs, files in os.walk(sourcedir):
                for item in files:
                    filename, ext = os.path.splitext(item)
                    ext = ext[1:]
                    if not filename.startswith('_') and \
                       ext in self.FINDER_COMPILABLE_EXTS:
                            filepaths.append(os.path.join(root, item))
                # For non recursive usage, break from the first entry
                if not recursive:
                    break

        return filepaths
