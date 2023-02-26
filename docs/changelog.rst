.. _click: http://click.pocoo.org/6/

=========
Changelog
=========

Version 2.1.0 - Unreleased
--------------------------

* Added new option ``HASH_SUFFIX`` to append a hash suffix to built filenames, thanks
  to `@arichr <https://github.com/arichr>`_ for its contribution;
* Changed ``setup.cfg`` to move every requirements that are not useful for tests into
  a new extra requirement ``[quality]`` so Tox will be faster to install without
  useless requirements. The Makefile install task still install everything;
* Update install documentation to close issues #39 and #40;


Version 2.0.0 - 2021/02/07
--------------------------

*Drop Python2 support, change configuration filename and some minor improvements*

* **[Backward incompatible]** Drop Python2 support (remove six, unicode litteral,
  update package configuration, etc..);
* **[Backward incompatible]** Changed default configuration filename from
  ``settings`` to ``boussole``. This was required to avoid clash with some other
  projects since "settings" is a too common word;
* Drop ``pathtools`` package dependency since it is an abandoned project;
* Update doc config, use livereload and with new RTD config file;
* Drop support for libsass-python ``<0.19.4``.
* Rename ``requirements_freeze.txt`` to ``frozen.txt``;
* Add a new script for development which help to automatically update the
  ``frozen.txt`` file;

For new configuration filename change you have two way to resolve it:

* Just change your configuration filename to the new one, like if you were
  using ``settings.json``, you will rename it to ``boussole.json``;
* Use option ``--config`` to explicitely use your own configuration filename;


Version 1.6.0 - 2021/02/04
--------------------------

*Last Python2 support, compatibility for recent Click versions and improve
performance*

**This will be the last version with Python2 support. A next release will come
soon to remove its support and focus on Python3 only.** This will may also drop
support for old Click and libsass versions.

Click requirement has been relaxed to only require for version greater or equal
to ``5.1.0``. This has been currently tested to ``7.1.2`` so it's surely safe
from 5.x to 7.x versions.

Watcher has been modified to avoid performing indexation on every event and
every file. It should give a few performance improvements and also avoid a bug
with editors making a transition writing file when saving modification (like
a ``foo.scss.part`` when writing on ``foo.scss``) which may leaded to incorrect
errors.

Version 1.5.1 - 2020/05/17
--------------------------

*Minor update to improve quality on development*

Since libsass-python 0.19.4, a new minor feature has been added which add the
column position in some error messages. This was breaking tests but without any
impact in Boussole functioning.

For sanity, we added a minor check against libsass-python version in a test to
continue support for libsass-python from 0.18.x to 0.20.x versions. It adds a
new dependency to ``packaging`` package only in development requirements.

Finally the Tox configuration has been updated to perform tests against supported
libsass-python versions and flake coverage has been done on tests.

Version 1.5.0 - 2019/05/17
--------------------------

**Indented Sass syntax support and fix some warnings**

Fixed warning from libsass-python about 'custom_import_extensions'
..................................................................

Libsass has reverted its previous change from version 3.5.3 which ignored CSS
files on default. This has required to add a new option
``CUSTOM_IMPORT_EXTENSIONS`` in Boussole 1.2.3 to enable CSS files support.

Since CSS support is back again on default, we removed useless setting
``CUSTOM_IMPORT_EXTENSIONS`` and don't use anymore
``custom_import_extensions`` argument with libsass-python compiler.

This remove previous warning from libsass-python about
``custom_import_extensions`` deprecation.

Fixed PyYAML 'load()' deprecation warning
.........................................

For a recent security issue, PyYAML has introduced a change to its ``load()``
method to be more safe.

We now use the full loader mode so it does not trigger a warning anymore.

Indented Sass syntax support
............................

Boussole should now be able to manage projects writed with the
`old indented syntax <https://sass-lang.com/documentation/syntax#the-indented-syntax>`_
(in files with extension ``*.sass``).

There is only one issue which blocking Boussole to manage ``@import`` rules on
multiple lines like: ::

    // Sample
    @import foo,
            bar

    // something

So you will need to change these imports to make a single ones on their own
lines: ::

    // Sample
    @import foo
    @import bar

    // something

Without this, watch command will miss some import directives. Compile command
should work normally since it does not involve source parsing.

Also, multiline comments are not supported. It will lead to false positives if
there are ``@import`` rules inside a multiline comments, causing these rules to
be taken as correct imports to check for.

Version 1.4.1 - 2018/10/21
--------------------------

**Fixed packaging**

``setup.py`` has been forgotted from previous release and still contained
information.

So it has been cleaned an ``setup.cfg`` has been updated to include missing
``[options.entry_points]`` section.

Version 1.4.0 - 2018/10/01
--------------------------

**Improved packaging**

We moved every package informations into ``setup.cfg`` and now ``setup.py`` is
only an entrypoint for setuptools. tox and pytest configurations has been
moved also into ``setup.cfg``.

Makefile has been updated and python-venv has been dropped in profit of
virtualenv to ease development.

Version 1.3.0 - 2018/09/30
--------------------------

**Add settings file discovering**

Introduce a new way to load settings file with a discovering which either just
load given an explicit file path or try to find it from base directory and
available settings backends.

This should not include backward incompatible behavior, it just adds capacity
to find another backend default filename kind.

Concretely, before this release only ``settings.json`` would be finded when no
explicit file path was given and now it will be able to find also a file
``settings.yml`` if it exists in current directory.

Version 1.2.3 - 2018/05/20
--------------------------

* **Introduced new settings** ``CUSTOM_IMPORT_EXTENSIONS`` which default value
  is ``['.css']`` to keep CSS source including behavior as default just like
  before libsass==3.5.3, close #29;
* Fixed source map url, close #28;

Version 1.2.2 - 2017/12/12
--------------------------

* Removed ``pytest-catchlog`` from tests requirements since it has been merged
  in ``pytest==3.3.0``;
* Upgraded to ``pytest>=3.3.0`` in tests requirements;

Version 1.2.1 - 2017/11/15
--------------------------

* Updated Makefile and development document to add everything for development
  install;
* Validated tests with ``libsass==0.13.4``;
* Document watcher behavior about inspection, close #24;

Version 1.2.0 - 2017/01/21
--------------------------

* Fixed pytest warning about deprecated section name in ``setup.cfg``;
* Updated tests requirements;
* Removed python 3.4 from tox envs;
* Added ``--poll`` option on watch command to use Watchdog polling observer
  instead of the native platform observer, close #22;
* Fixed compiler tests for changes about source map since last libsass version;
* Fixed Sass brand name according to http://sassnotsass.com/;
* Validated tests with ``libsass==0.12.3``;

Version 1.1.0 - 2016/11/26
--------------------------

* YAML backend for settings, close #7 :

  * Added ``yaml_backend.SettingsBackendYaml`` backend;
  * Implement YAML backend in unittests;
  * Added helper to discover settings backend from filename extension;
  * Configuration backend now implement a dump method;
  * Changed ``project.ProjectStarter`` so it can load Configuration backend;

* Don't pass anymore logger to objects, just use
  ``logging.getLogger("boussole")``, close #11;
* Validate tests on Python 3.5 through tox;


Version 1.0.2 - 2016/10/26
--------------------------

Upgrade ``libsass-python`` dependency to ``>=0.11.2`` to profit from
``libsass==3.3.6`` (include bugfix for segfault with ``@extends`` and ``:not``);

Version 1.0.1 - 2016/09/10
--------------------------

Fixed encoding issue with inspector that leaded to some bugs with watcher,
close #17;

Version 1.0.0 - 2016/08/01
--------------------------

Added Python 3.4 support, thanks to `@feth <https://github.com/feth>`_ for its
contributions.

* Added ``six`` as requirement;
* Use the 'key' param in sorted: 'cmp' is removed

    * Factored out the calls to sorted into paths_by_depth.
    * removed path_parts_cmp, used by removed keyword arg cmp (replaced by a
      lambda function);

* More pythonic way of checking the match in Finder;
* Fixed parser.py for ``filter`` builtin function usage;
* Use StringIO object from 'io' module instead of deprecated 'StringIO' module;
* Don't use anymore ``message`` class attribute with Exceptions;
* Don't open JSON settings file with ``rb`` inside tests, mode ``r`` is enough;
* Fixed ``os.listdir`` usage in tests (using sorted results);
* Fixed logging messages to be unicode string;
* Added Python 3.4 interpreter in available tox environments;

Version 0.9.2 - 2016/07/30
--------------------------

Fixed some tests related to directory/files structures that were not
consistant because of ``os.walk`` arbitrary order, close #16;

Version 0.9.1 - 2016/07/29
--------------------------

* Added tox configuration file starting with Python2.7;
* Fixed some postprocessor that was failing because of usage of
  ``os.envrion['HOME']`` not working inside tox env;
* Disabled ``flake8-format-ansi`` since it seems to cause errors in some cases,
  it is recommended to do ``pip uninstall flake8-format-ansi`` for now;
* Fixed some inspector tests failing on some wrong result orders because of
  ``set()`` vs ``list()``;
* Fixed setup.py so tests directory is not installed anymore as a Python
  packages;
* Updated development documentation;

Version 0.9.0 - 2016/05/01
--------------------------

* Added new settings to enabled sourcemap generation, close #6;
* Finalize documentation, close #10

Version 0.8.3 - 2016/04/23
--------------------------

* New CLI action to start a project, close #8;
* Added logo to documentation;

Version 0.8.0 - 2016/04/16
--------------------------

* Relaxed ``libsass`` version in requirements;
* Moved ``colorama`` from test to default requirements;
* Removed every use of click.echo/secho within core API, use logger instead,
  close #1;
* Added ``colorlog`` in requirements and use it to have colors for each
  logging level, close #4;
* Changed verbosity option on CLI action so default verbosity is INFO logging
  level, then user can choose totally silent verbosity or any other logging
  level, definitively close #1;
* Better CLI actions helps, close #5;
* Manage every API exception from CLI, should be ok now (in fact since previous
  commit), close #3;
* Break unittests into subdirectories per module, close #9;

  * A subdirectory per module;
  * Renamed test files to be less verbose;
  * Renamed test functions to be less verbose;

* Added some settings validation, close #2;

Version 0.7.0 - 2016/04/07
--------------------------

This is almost near Beta version.

* Fixed a bug with comment removal from parser: url protocol separator (the
  ``//`` in ``http://``) was matched and leaded to errors in import rule
  parsing;
* Added ``logs`` module;
* Removed ``--config`` commandline option from console script entry point
  because some cli actions don't need to load a settings. Until i find a way to
  disable it for some action, the option will have to be duplicated on each
  action that require it (sic);
* Added ``flake8-format-ansi`` as a development requirement and use it in
  ``setup.cfg``;
* Added Unittests for ``compile`` commandline action;
* Added ``compiler`` module for some helper on top of ``libsass-python``
  compiler;
* Improved finder to have a common method to match conditions on filepath (is
  partial, is allowed, etc..);
* Added new exception ``FinderException``;
* Unittest for Watcher event handler (but not on ``watch`` commandline because
  of some limit from click ``CliRunner``)
* Added ``pytest-catchlog`` plugin to have nice logging management within tests;
* Moved flake8 config to ``.flake8`` instead of ``setup.cfg`` since
  ``flake8-format-ansi`` plugin config cause issues with ``pytest-catchlog``
  install;
* Finished working version for command line action ``watch``;
* Updated documentation;

Version 0.6.0 - 2016/03/25
--------------------------

* Modified conf backend to be more flexible with given base dir and file path;
* Accorded settings manifest to ``libsass-python`` compiler options;
* Finished first working version for command line action ``compile``;
* Upgraded ``libsass-python`` requirement to version ``0.11.0``
* Improved command line action ``version`` to include both ``libsass-python``
  and ``libsass`` versions;

Version 0.5.0 - 2016/03/19
--------------------------

* Added CLI structure with `click`_;
* Lowered click version requirement to 5.1 (since 6.x is not stable yet);
* Restructured tests for conf module and added some new ones for Settings
  object;
* Moved all settings files up the sample project;
* Finished conf management;

Version 0.4.0 - 2016/03/14
--------------------------

* Added ``conf`` module to manage project settings;
* Doc, flake8, unittests for ``conf``;

Version 0.3.0 - 2016/03/10
--------------------------

* Added ``finder`` module;
* Doc, flake8, unittests for ``finder``;

Version 0.2.0 - 2016/03/09
--------------------------

Finished changes for the right path resolving/checking behavior with unclear
resolutions;

Version 0.1.0 - 2016/03/06
--------------------------

* Made changes to pass Flake8 validation on API;
* Started Sphinx documentation;

Version 0.0.9.5 - 2016/03/06
----------------------------

* Document core using Sphinx+Napoleon syntax;
* Cleaned all debug pointers;
* Minor improvements;
* Added some last inspector tests;

Version 0.0.9 - 2016/03/05
----------------------------

* Finished inspector to detect almost all circular import;
* Improved tests;
* Did some cleaning;
* Still need some debug pointer cleaning and then documentation;

Version 0.0.8 - 2016/03/01
--------------------------

* Updated project to use pytest for unittests;
* updated unittests to fit to pytest usage;
* Added first inspector tests;

Version 0.0.7 - 2016/02/29
--------------------------

* Improved tests;
* Finished working inspector but not unittested yet;

Version 0.0.6 - 2016/02/25
--------------------------

* Added inspector
* Improved parser to remove comments before looking for import rules, this
  will avoid to catch commented import rules;
* Updated tests;
* Added click as requirement;

Version 0.0.5 - 2016/02/22
--------------------------

* Changed resolver behavior to return absolute instead of relative
* Fixed tests;

Version 0.0.4 - 2016/02/22
--------------------------

Finished stable and unittested parser and resolver;

Version 0.0.3 - 2016/02/21
--------------------------

Finished first resolver version, still need to do the library_paths thing;

Version 0.0.2 - 2016/02/21
--------------------------

* Improved test;
* Continued on resolver (was named validate previously);

Version 0.0.1 - 2016/02/20
--------------------------

First commit
