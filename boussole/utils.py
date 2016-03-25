# -*- coding: utf-8 -*-
"""
Utilities
=========

Some common and various utilities that don't fit elsewhere and not so
important to require their own module.
"""
import os
import io


def build_target_helper(content, path):
    """
    Write target file from given content to given destination path.

    It will create needed directory structure first if it contain some
    directories that does not allready exists.

    Args:
        content (str): Content to write to target file.
        path (str): Destination path for target file.

    Returns:
        str: Path where target file has been written.
    """
    directory = os.path.dirname(path)

    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    with io.open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    return path
