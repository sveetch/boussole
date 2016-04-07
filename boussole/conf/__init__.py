# -*- coding: utf-8 -*-
"""
Project configuration
=====================

Boussole work on per project configurations stored in a settings file for each
project.

Backends behavior is to search for a settings file in the given directory, read
it, possibly patch its values and hen return a
:class:`boussole.conf.model.Settings object`.

Almost all paths in settings will be expanded to absolute paths if they are
not allready so:

* If the path start with a home directory character, the home directory is used
  to expand the path;
* If the path is relative, expand it to absolute using directory from settings
  file location;

Also note, that SASS files from libraries directories are never compiled.
"""
import copy


# Settings manifest define default values and values patchs for each setting
SETTINGS_MANIFEST = {
    'LIBRARY_PATHS': {
        'default': [],
        'patchs': ['_patch_expand_paths'],
    },
    'SOURCES_PATH': {
        'default': None,
        'patchs': ['_patch_expand_path'],
    },
    'TARGET_PATH': {
        'default': None,
        'patchs': ['_patch_expand_path'],
    },
    'OUTPUT_STYLES': {
        'default': 'nested',
        'patchs': [],
    },
    'SOURCE_COMMENTS': {
        'default': False,
        'patchs': [],
    },
    'EXCLUDES': {
        'default': [],
        'patchs': [],
    },
}


# Default values for initial settings object
DEFAULT_SETTINGS = {k: copy.deepcopy(v['default'])
                    for k, v in SETTINGS_MANIFEST.items()}
