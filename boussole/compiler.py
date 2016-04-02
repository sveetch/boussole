# -*- coding: utf-8 -*-
"""
.. _libsass-python: https://github.com/dahlia/libsass-python

SASS compile helper
===================

This is not a real compiler, just an helper wrapping common methods to compile
a SASS source from a project using `libsass-python`_.
"""
import click
import os
import io

import sass


class SassCompileHelper(object):
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

        Todo:
            Maybe this can inherit from finder.

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
        try:
            content = sass.compile(
                filename=sourcepath,
                output_style=settings.OUTPUT_STYLES,
                source_comments=settings.SOURCE_COMMENTS,
                include_paths=settings.LIBRARY_PATHS,
            )
        except sass.CompileError as e:
            click.secho(e.message, fg='red')
            return False, e.message
        else:
            self.write_content(content, destination)
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
