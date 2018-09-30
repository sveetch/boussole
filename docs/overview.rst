.. _virtualenv: http://www.virtualenv.org
.. _pip: https://pip.pypa.io
.. _Pytest: http://pytest.org
.. _Napoleon: https://sphinxcontrib-napoleon.readthedocs.org
.. _Flake8: http://flake8.readthedocs.org
.. _libsass-python: https://github.com/dahlia/libsass-python

========
Overview
========

Boussole is working on **per-project configuration**, it means all your Sass sources to compile have to be organized in the same directory considered as the *sources directory*. Obviously you can organize them in multiple sub-directories within your sources directory.

Your project can rely on some **Sass libraries that must be out of the source directory** to be defined in option ``LIBRARY_PATHS``.

Boussole does not really handle itself compilation, this is the role of `libsass-python`_. But for watch mode Boussole needs to inspect your Sass sources and so can raise some errors if they are invalid. These errors will be almost only about your ``@import`` rules.

**Boussole is builded following Sass references** and all your Sass sources and libraries compatibles with libsass should be safe to compile.


Project configuration
*********************

A project **configuration lives in a file** which default attempted name is ``settings.json`` (JSON backend) or ``settings.yml`` (YAML backend).

Backend format
--------------

There is actually two supported backend format: JSON and YAML. Each of backend format expect is own default filename.

However you can ask for a specific backend from command line use argument ``--backend``, value can be either ``json`` or ``yaml``.

Discovering
-----------

Boussole is able to discover your settings file if you don't explicitely give it as command argument with ``--config`` option.

Discovering is allways performed from current directory and will try to find a settings file using available backend default filename.

Such as if you have a ``settings.yml`` in your current directory, Boussole will assume it's your settings file to open. JSON backend is the first one to be checked so if you have both ``settings.json`` and ``settings.yml`` in your current directory, the JSON will be used.

You may possibly enforce a single backend to be used in discovery using the ``--backend`` option.

Finally, if you give an explicit settings file path with ``--config`` there will be no discovering, Boussole will just open it directly.

Sample
------

Here is a full sample of available settings for project configuration with JSON format:

    .. sourcecode:: json

        {
            "SOURCES_PATH": "/home/foo",
            "LIBRARY_PATHS": [
                "/home/lib1",
                "/home/lib2"
            ],
            "TARGET_PATH": "/home/bar",
            "OUTPUT_STYLES": "nested",
            "CUSTOM_IMPORT_EXTENSIONS": [
                ".css"
            ],
            "SOURCE_COMMENTS": false,
            "SOURCE_MAP": false,
            "EXCLUDES": [
                "*/*.backup.scss",
                "/home/lib2"
            ]
        }

References
----------

.. Note::
    Default values are referenced as Python values, you will need to adapt them according to the backend format you are using.


SOURCES_PATH
    Default: ``None``, this is a required setting.

    (string) Path to the directory containing your project Sass sources to compile.
LIBRARY_PATHS
    Default: ``[]``

    (list) A list of paths (string) to your library imported from your Sass sources. Never try to add your source dir as a library and vice versa, this will trouble resolver and compiler.
TARGET_PATH
    Default: None, this is a required setting.

    (string) Directory path where will be writed your compiled Sass sources.
OUTPUT_STYLES
    Default: ``nested``

    (string) keyword of output style type used to compile your Sass sources. Can be either ``compact``, ``expanded``, ``nested`` or ``compressed``.
CUSTOM_IMPORT_EXTENSIONS
    Default: ``[".css"]``

    (list) List of enabled source extensions allowed to be included from ``@import`` directive. This aims to allow to treat some sources as Sass source to include. Default value is made so using ``@import 'foo'`` will include ``foo.css`` source if it exists. Set an empty list if you want to only allow Sass source extensions.
SOURCE_COMMENTS
    Default: ``False``

    (boolean) If ``True``, comments about source lines will be added to each rule in resulted CSS from compile.
SOURCE_MAP
    Default: ``False``

    (boolean) If ``True``, generate a source map for each compiled file. Source map filename will be the same that compiled file but with extension changed to ``.map``. The source map file is allways created in the same directory than CSS file.
EXCLUDES
    Default: ``[]``

    (list) A list of glob pattern (string) to exclude some paths/files from compile. Remember these pattern are allways matched against relative paths (from project directory).


Help
****

You can read help about global options with: ::

    boussole -h

And you can reach help about command options using: ::

    boussole [command name] -h


Start a new project
*******************

Create directory and configuration file for a new project. Although you can create your project manually, this is an easy helper to do it and avoid forgetting some details.

Without arguments, command will prompt you to fill required values but you can also directly feed these values from arguments, see command help for details.

**Usage** ::

    boussole startproject


Compile
*******

Compile simply launch compiler on every eligible Sass source from your ``SOURCES_PATH`` directory.

**Usage** ::

    boussole compile


Watch
*****

Watcher will constantly watch about changes on files in your ``SOURCES_PATH`` directory.

When an event occurs, it will compile eligible sources from the file dependencies and itself. Managed events can be :

* File creation;
* File modification;
* File move;
* File deletion.

.. Note::
    Compile errors won't break the watcher, meaning you can resolve them and it will try again to compile.


**Usage** ::

    boussole watch

.. Note::
    Default behavior is to use the Watchdog native platform observer. It may not work for all environments (like on shared directories through network or Virtual machine), in this case use the ``--poll`` to use the Watchdog polling observer instead of the default one.

Boussole has its own internal code to inspect Sass sources to be aware of sources paths it has to watch for.

It results inspection does not have exactly the same path resolution process than libsass.

It can lead to troubleshooting situations where ``compile`` command can build some sources that can fails with ``watch`` command because the latter need to inspect sources to be able to find dependencies and choke on unclear path resolution.

These unclear paths are almost allways due to some Sass libraries trying to import components using a relative path outside of itself like with ``../``. This is often the case with libraries that have been made to be included in your main scss directory.
