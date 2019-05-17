# -*- coding: utf-8 -*-
"""
.. _libsass-python: https://github.com/dahlia/libsass-python

Sass compile helper
===================

This is not a real compiler, just an helper wrapping common methods to compile
a Sass source using `libsass-python`_.
"""
import os
import io

import six

import sass

from boussole.finder import ScssFinder


class SassCompileHelper(ScssFinder):
    """
    Sass compile helper mixin
    """
    def safe_compile(self, settings, sourcepath, destination):
        """
        Safe compile

        It won't raise compile error and instead return compile success state
        as a boolean with a message.

        It will create needed directory structure first if it contain some
        directories that does not allready exists.

        Args:
            settings (boussole.conf.model.Settings): Project settings.
            sourcepath (str): Source file path to compile to CSS.
            destination (str): Destination path for compiled CSS.

        Returns:
            tuple: A tuple of (success state, message).

            * success state: is boolean weither the compile is a success
              or not;
            * message: Message accorded to success. If compile fails, the
              message will contains returned error from libsass, if success
              just the destination path.
        """
        source_map_destination = None
        if settings.SOURCE_MAP:
            source_map_destination = self.change_extension(destination, "map")

        try:
            content = sass.compile(
                filename=sourcepath,
                output_style=settings.OUTPUT_STYLES,
                source_comments=settings.SOURCE_COMMENTS,
                include_paths=settings.LIBRARY_PATHS,
                # Sourcemap is allways in the same directory than compiled
                # CSS file
                output_filename_hint=destination,
                source_map_filename=source_map_destination,
            )
        except sass.CompileError as e:
            return False, six.text_type(e)
        else:
            # Compiler return a tuple (css, map) if sourcemap is
            # enabled
            sourcemap = None
            if settings.SOURCE_MAP:
                content, sourcemap = content

            self.write_content(content, destination)

            # Write sourcemap if any
            if sourcemap:
                self.write_content(sourcemap, source_map_destination)

            return True, destination

    def write_content(self, content, destination):
        """
        Write given content to destination path.

        It will create needed directory structure first if it contain some
        directories that does not allready exists.

        Args:
            content (str): Content to write to target file.
            destination (str): Destination path for target file.

        Returns:
            str: Path where target file has been written.
        """
        directory = os.path.dirname(destination)

        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        with io.open(destination, 'w', encoding='utf-8') as f:
            f.write(content)

        return destination
