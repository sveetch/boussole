# -*- coding: utf-8 -*-
"""
Project configuration
=====================

Boussole work on per project configurations stored in a settings file for each
project.

Backends behavior is to search for a settings file in the given directory, read
it, possibly patch its values and then return a
:class:`boussole.conf.model.Settings object`.

Almost all paths in settings will be expanded to absolute paths if they are
not allready so:

* If the path start with a home directory character, the home directory is used
  to expand the path;
* If the path is relative, expand it to absolute using directory from settings
  file location;

Also note, that Sass files from libraries directories are never compiled.
"""
# Manifest define default values and post process methods for each setting
# Warning: Order does matter on "postprocess" methods
SETTINGS_MANIFEST = {
    'LIBRARY_PATHS': {
        'default': [],
        'postprocess': (
            '_patch_expand_paths',
            '_validate_paths',
        ),
    },
    'SOURCES_PATH': {
        'default': None,
        'postprocess': (
            '_validate_required',
            '_patch_expand_path',
            '_validate_path',
        ),
    },
    'TARGET_PATH': {
        'default': None,
        'postprocess': (
            '_validate_required',
            '_patch_expand_path',
            '_validate_path',
        ),
    },
    'OUTPUT_STYLES': {
        'default': 'nested',
        'postprocess': [],
    },
    'SOURCE_COMMENTS': {
        'default': False,
        'postprocess': [],
    },
    'CUSTOM_IMPORT_EXTENSIONS': {
        'default': ['.css'],
        'postprocess': [],
    },
    'SOURCE_MAP': {
        'default': False,
        'postprocess': [],
    },
    'EXCLUDES': {
        'default': [],
        'postprocess': [],
    },
}
