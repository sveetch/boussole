# -*- coding: utf-8 -*-
"""
.. _Sass partials Reference:
    http://sass-lang.com/documentation/file.SASS_REFERENCE.html#partials

Finder
======

Finder is in charge to find *main Sass stylesheets* files to compile to CSS
files, meaning it will ignore all partials Sass stylesheets (see
`Sass partials Reference`_).

"""
import fnmatch
import os

from boussole.exceptions import FinderException


def paths_by_depth(paths):
    """Sort list of paths by number of directories in it

    .. todo::

        check if a final '/' is consistently given or ommitted.

    :param iterable paths: iterable containing paths (str)
    :rtype: list
    """
    return sorted(
            paths,
            key=lambda path: path.count(os.path.sep),
            reverse=True
    )


class ScssFinder(object):
    """
    Project finder for SCSS sources

    Attributes:
        FINDER_STYLESHEET_EXTS: List of file extensions regarded as
            compilable stylesheet sources.
    """
    FINDER_STYLESHEET_EXTS = ['scss', ]

    def get_relative_from_paths(self, filepath, paths):
        """
        Find the relative filepath from the most relevant multiple paths.

        This is somewhat like a ``os.path.relpath(path[, start])`` but where
        ``start`` is a list. The most relevant item from ``paths`` will be used
        to apply the relative transform.

        Args:
            filepath (str): Path to transform to relative.
            paths (list): List of absolute paths to use to find and remove the
                start path from ``filepath`` argument. If there is multiple
                path starting with the same directories, the biggest will
                match.

        Raises:
            boussole.exception.FinderException: If no ``filepath`` start could
            be finded.

        Returns:
            str: Relative filepath where the start coming from ``paths`` is
                removed.
        """
        for systempath in paths_by_depth(paths):
            if filepath.startswith(systempath):
                return os.path.relpath(filepath, systempath)

        raise FinderException("'Finder.get_relative_from_paths()' could not "
                              "find filepath start from '{}'".format(filepath))

    def is_partial(self, filepath):
        """
        Check if file is a Sass partial source (see
        `Sass partials Reference`_).

        Args:
            filepath (str): A file path. Can be absolute, relative or just a
            filename.

        Returns:
            bool: True if file is a partial source, else False.
        """
        path, filename = os.path.split(filepath)
        return filename.startswith('_')

    def is_allowed(self, filepath, excludes=[]):
        """
        Check from exclude patterns if a relative filepath is allowed

        Args:
            filepath (str): A relative file path. (exclude patterns are
                allways based from the source directory).

        Keyword Arguments:
            excludes (list): A list of excluding (glob) patterns. If filepath
                matchs one of patterns, filepath is not allowed.

        Raises:
            boussole.exception.FinderException: If given filepath is absolute.

        Returns:
            str: Filepath with new extension.
        """
        if os.path.isabs(filepath):
            raise FinderException("'Finder.is_allowed()' only accept relative"
                                  " filepath")

        if excludes:
            for pattern in excludes:
                if fnmatch.fnmatch(filepath, pattern):
                    return False
        return True

    def match_conditions(self, filepath, sourcedir=None, nopartial=True,
                         exclude_patterns=[], excluded_libdirs=[]):
        """
        Find if a filepath match all required conditions.

        Available conditions are (in order):

        * Is allowed file extension;
        * Is a partial source;
        * Is from an excluded directory;
        * Is matching an exclude pattern;

        Args:
            filepath (str): Absolute filepath to match against conditions.

        Keyword Arguments:
            sourcedir (str or None): Absolute sources directory path. Can be
                ``None`` but then the exclude_patterns won't be matched against
                (because this method require to distinguish source dir from lib
                dirs).
            nopartial (bool): Accept partial sources if ``False``. Default is
                ``True`` (partial sources fail matchind condition). See
                ``Finder.is_partial()``.
            exclude_patterns (list): List of glob patterns, if filepath match
                one these pattern, it wont match conditions. See
                ``Finder.is_allowed()``.
            excluded_libdirs (list): A list of directory to match against
                filepath, if filepath starts with one them, it won't
                match condtions.

        Returns:
            bool: ``True`` if match all conditions, else ``False``.
        """
        # Ensure libdirs ends with / to avoid missmatching with
        # 'startswith' usage
        excluded_libdirs = [os.path.join(d, "") for d in excluded_libdirs]

        # Match an filename extension admitted as compilable stylesheet
        filename, ext = os.path.splitext(filepath)
        ext = ext[1:]
        if ext not in self.FINDER_STYLESHEET_EXTS:
            return False

        # Not a partial source
        if nopartial and self.is_partial(filepath):
            return False

        # Not in an excluded directory
        if any(
            filepath.startswith(excluded_path)
            for excluded_path in paths_by_depth(excluded_libdirs)
        ):
            return False

        # Not matching an exclude pattern
        if sourcedir and exclude_patterns:
            candidates = [sourcedir]+excluded_libdirs
            relative_path = self.get_relative_from_paths(filepath, candidates)
            if not self.is_allowed(relative_path, excludes=exclude_patterns):
                return False

        return True

    def change_extension(self, filepath, new_extension):
        """
        Change final filename extension.

        Args:
            filepath (str): A file path (relative or absolute).
            new_extension (str): New extension name (without leading dot) to
                apply.

        Returns:
            str: Filepath with new extension.
        """
        filename, ext = os.path.splitext(filepath)
        return '.'.join([filename, new_extension])

    def get_destination(self, filepath, targetdir=None):
        """
        Return destination path from given source file path.

        Destination is allways a file with extension ``.css``.

        Args:
            filepath (str): A file path. The path is allways relative to
                sources directory. If not relative, ``targetdir`` won't be
                joined.
            absolute (bool): If given will be added at beginning of file
                path.

        Returns:
            str: Destination filepath.
        """
        dst = self.change_extension(filepath, 'css')
        if targetdir:
            dst = os.path.join(targetdir, dst)
        return dst

    def compilable_sources(self, sourcedir, absolute=False, recursive=True,
                           excludes=[]):
        """
        Find all scss sources that should be compiled, aka all sources that
        are not "partials" Sass sources.


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
            # Sort structure to avoid arbitrary order
            dirs.sort()
            files.sort()
            for item in files:
                # Store relative directory but drop it if at root ('.')
                relative_dir = os.path.relpath(root, sourcedir)
                if relative_dir == '.':
                    relative_dir = ''

                # Matching all conditions
                absolute_filepath = os.path.join(root, item)
                conditions = {
                    'sourcedir': sourcedir,
                    'nopartial': True,
                    'exclude_patterns': excludes,
                    'excluded_libdirs': [],
                }
                if self.match_conditions(absolute_filepath, **conditions):
                    relative_filepath = os.path.join(relative_dir, item)

                    if absolute:
                        filepath = absolute_filepath
                    else:
                        filepath = relative_filepath

                    filepaths.append(filepath)

            # For non recursive usage, break from the first entry
            if not recursive:
                break

        return filepaths

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
            list: A list of pairs ``(source, target)``. Where ``target`` is the
                ``source`` path but renamed with ``.css`` extension. Relative
                directory from source dir is left unchanged but if given,
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
            dst = self.get_destination(src, targetdir=targetdir)

            # In absolute mode
            if targetdir:
                src = os.path.join(sourcedir, src)

            maplist.append((src, dst))

        return maplist
