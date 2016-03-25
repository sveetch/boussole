# -*- coding: utf-8 -*-
"""
.. _SASS partials Reference:
    http://sass-lang.com/documentation/file.SASS_REFERENCE.html#partials

Finder
======

Finder is in charge to find *main SASS stylesheets* files to compile to CSS
files, meaning it will ignore all partials SASS stylesheets (see
`SASS partials Reference`_).

"""
import fnmatch
import os


class ScssFinder(object):
    """
    Project finder for SCSS sources

    Attributes:
        FINDER_COMPILABLE_EXTS: List of file extensions regarded as compilable
            sources.
    """
    FINDER_COMPILABLE_EXTS = ['scss', 'sass']

    def compilable_sources(self, sourcedir, absolute=False, recursive=True,
                           excludes=[]):
        """
        Find all scss sources that should be compiled, aka all sources that
        are not "partials" SASS sources.

        Args:
            sourcedir (str): Directory path to scan.

        Keyword Arguments:
            absolute (bool): Returned paths will be absolute using
                ``sourcedir`` argument (if True), else return relative paths.
            recursive (bool): Switch to enabled recursive finding (if True).
                Default to True.
            excludes (list): A list of excluding patterns (glob patterns).
                Patterns are matched against the relative filepath (from its
                sourcedir).

        Returns:
            list: List of source paths.

        """
        filepaths = []

        for root, dirs, files in os.walk(sourcedir):
            for item in files:
                filename, ext = os.path.splitext(item)
                # Drop extension starting dot
                ext = ext[1:]
                # Store relative directory but drop it if at root ('.')
                relative_dir = os.path.relpath(root, sourcedir)
                if relative_dir == '.':
                    relative_dir = ''
                # Matching conditions
                if not filename.startswith('_') and \
                   ext in self.FINDER_COMPILABLE_EXTS:
                        absolute_filepath = os.path.join(root, item)
                        relative_filepath = os.path.join(relative_dir, item)

                        if absolute:
                            filepath = absolute_filepath
                        else:
                            filepath = relative_filepath
                        # Excluding patterns verification
                        if self.is_allowed(relative_filepath,
                                           excludes=excludes):
                            filepaths.append(filepath)

            # For non recursive usage, break from the first entry
            if not recursive:
                break

        return filepaths

    def is_allowed(self, filepath, excludes=[]):
        """
        Check from exclude patterns if filepath is allowed

        Args:
            filepath (str): A file path.

        Keyword Arguments:
            excludes (list): A list of excluding patterns. If filepath matchs
                one of patterns, filepath is not allowed.

        Returns:
            str: Filepath with new extension.
        """
        if excludes:
            for pattern in excludes:
                if fnmatch.fnmatch(filepath, pattern):
                    return False
        return True

    def change_extension(self, filepath, new_extension):
        """
        Change final filename extension.

        Args:
            filepath (str): A file path.
            new_extension (str): New extension name (without leading dot) to
                apply.

        Returns:
            str: Filepath with new extension.
        """
        filename, ext = os.path.splitext(filepath)
        return '.'.join([filename, new_extension])

    def mirror_sources(self, sourcedir, targetdir=None, recursive=True,
                       excludes=[]):
        """
        Mirroring compilable sources filepaths to their targets.

        Args:
            sourcedir (str): Directory path to scan.

        Keyword Arguments:
            absolute (bool): Returned paths will be absolute using
                ``sourcedir`` argument (if True), else return relative paths.
            recursive (bool): Switch to enabled recursive finding (if True).
                Default to True.
            excludes (list): A list of excluding patterns (glob patterns).
                Patterns are matched against the relative filepath (from its
                sourcedir).

        Returns:
            list: A list of pairs ``(source, target)``. Where ``target``
                will be renamed with ``.css`` extension. Relative directory
                from source dir is left unchanged, but if  is given
                returned paths will be absolute (using ``sourcedir`` for
                sources and ``targetdir`` for targets).
        """
        sources = self.compilable_sources(
            sourcedir,
            absolute=False,
            recursive=recursive,
            excludes=excludes
        )
        maplist = []

        for filepath in sources:
            src = filepath
            dst = self.change_extension(filepath, 'css')

            # For absolute mode
            if targetdir:
                src = os.path.join(sourcedir, src)
                dst = os.path.join(targetdir, dst)

            maplist.append((src, dst))

        return maplist
