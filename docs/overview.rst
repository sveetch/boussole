.. _virtualenv: http://www.virtualenv.org
.. _pip: https://pip.pypa.io
.. _Pytest: http://pytest.org
.. _Napoleon: https://sphinxcontrib-napoleon.readthedocs.org
.. _Flake8: http://flake8.readthedocs.org
.. _libsass-python: https://github.com/dahlia/libsass-python

========
Overview
========

Boussole is working on **per-project configuration**, it means all your SASS sources to compile have to be organized in the same directory considered as the *sources directory*. Obviously you can organize them in multiple sub-directories within your sources directory.

Your project can rely on some **SASS libraries that must be out of the source directory**.

Boussole does not really handle itself compilation, this is the role of `libsass-python`_. But Boussole needs to inspect your SASS sources and so can raise some errors if they are invalid. These errors are almost only about your ``@import`` rules.

**Boussole is builded following SASS references** and all your SASS sources and libraries compatible with libsass should be safe to compile.

Project configuration
*********************

A project **configuration lives in a JSON file** which default attempted name is ``settings.json`` from current directory. You can use the argument ``--config`` to specify another path to your settings file.

It does not matter the filename of your file is ``settings.json`` or ``foo.json`` or anything else, but your file has to be a valid JSON file.

Sample
------

Here is a full sample of available settings for project configuration:

    .. sourcecode:: json

        {
            "SOURCES_PATH": "/home/foo",
            "LIBRARY_PATHS": [
                "/home/lib1",
                "/home/lib2"
            ],
            "TARGET_PATH": "/home/bar",
            "OUTPUT_STYLES": "nested",
            "SOURCE_COMMENTS": false,
            "EXCLUDES": [
                "*/*.backup.scss",
                "/home/lib2"
            ]
        }

References
----------

SOURCES_PATH
    Default: None, this is a required setting.

    (string) Path to the directory containing your project SASS sources to compile.
LIBRARY_PATHS
    Default: Empty list

    (list) A list of paths (string) to your library imported from your SASS sources. Never try to add your source dir as a library and vice versa, this will trouble resolver and compiler.
TARGET_PATH
    Default: None, this is a required setting.

    (string) Directory path where will be writed your compiled SASS sources.
OUTPUT_STYLES
    Default: ``nested``

    (string) keyword of output style type used to compile your SASS sources. Can be either ``compact``, ``expanded``, ``nested`` or ``compressed``.
SOURCE_COMMENTS
    Default: ``false``

    (boolean) If ``true``, comments about source lines will be added to each rule in resulted CSS from compile.
EXCLUDES
    Default: Empty list

    (list) A list of glob pattern (string) to exclude some paths/files from compile. Remember these pattern are allways matched against relative paths (from project directory).

Compile
*******

Use: ::

    boussole compile

Compile simply launch compiler on every eligible SASS source from your ``SOURCES_PATH``.

Watch
*****

Use: ::

    boussole watch

Watcher will constantly watch about changes on files in your ``SOURCES_PATH``. When a change event occurs, it will compile eligible sources from the file dependencies and itself.
