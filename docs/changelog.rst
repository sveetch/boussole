.. _click: http://click.pocoo.org/6/

=========
Changelog
=========

Version 0.9.1 - 2016/07/29
--------------------------

* Added tox configuration file starting with Python2.7;
* Fixed some postprocessor that was failing because of usage of ``os.envrion['HOME']`` not working inside tox env;
* Disabled ``flake8-format-ansi`` since it seems to cause errors in some cases, it is recommended to do ``pip uninstall flake8-format-ansi`` for now;
* Fixed some inspector tests failing on some wrong result orders because of ``set()`` vs ``list()``;
* Fixed setup.py so tests directory is not installed anymore as a Python packages;
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
* Removed every use of click.echo/secho within core API, use logger instead, close #1;
* Added ``colorlog`` in requirements and use it to have colors for each logging level, close #4;
* Changed verbosity option on CLI action so default verbosity is INFO logging level, then user can choose totally silent verbosity or any other logging level, definitively close #1;
* Better CLI actions helps, close #5;
* Manage every API exception from CLI, should be ok now (in fact since previous commit), close #3;
* Break unittests into subdirectories per module, close #9;

  * A subdirectory per module;
  * Renamed test files to be less verbose;
  * Renamed test functions to be less verbose;

* Added some settings validation, close #2;

Version 0.7.0 - 2016/04/07
--------------------------

This is almost near Beta version.

* Fixed a bug with comment removal from parser: url protocol separator (the ``//`` in ``http://``) was matched and leaded to errors in import rule parsing;
* Added ``logs`` module;
* Removed ``--config`` commandline option from console script entry point because some cli actions don't need to load a settings. Until i find a way to disable it for some action, the option will have to be duplicated on each action that require it (sic);
* Added ``flake8-format-ansi`` as a development requirement and use it in ``setup.cfg``;
* Added Unittests for ``compile`` commandline action;
* Added ``compiler`` module for some helper on top of ``libsass-python`` compiler;
* Improved finder to have a common method to match conditions on filepath (is partial, is allowed, etc..);
* Added new exception ``FinderException``;
* Unittest for Watcher event handler (but not on ``watch`` commandline because of some limit from click ``CliRunner``)
* Added ``pytest-catchlog`` plugin to have nice logging management within tests;
* Moved flake8 config to ``.flake8`` instead of ``setup.cfg`` since ``flake8-format-ansi`` plugin config cause issues with ``pytest-catchlog`` install;
* Finished working version for command line action ``watch``;
* Updated documentation;

Version 0.6.0 - 2016/03/25
--------------------------

* Modified conf backend to be more flexible with given base dir and file path;
* Accorded settings manifest to ``libsass-python`` compiler options;
* Finished first working version for command line action ``compile``;
* Upgraded ``libsass-python`` requirement to version ``0.11.0``
* Improved command line action ``version`` to include both ``libsass-python`` and ``libsass`` versions;

Version 0.5.0 - 2016/03/19
--------------------------

* Added CLI structure with `click`_;
* Lowered click version requirement to 5.1 (since 6.x is not stable yet);
* Restructured tests for conf module and added some new ones for Settings object
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

* Finished changes for the right path resolving/checking behavior with unclear resolutions;

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
* Improved parser to remove comments before looking for import rules, this will avoid to catch commented import rules;
* Updated tests;
* Added click as requirement;

Version 0.0.5 - 2016/02/22
--------------------------

* Changed resolver behavior to return absolute instead of relative
* Fixed tests;

Version 0.0.4 - 2016/02/22
--------------------------

* Finished stable and unittested parser and resolver;

Version 0.0.3 - 2016/02/21
--------------------------

* Finished first resolver version, still need to do the library_paths thing;

Version 0.0.2 - 2016/02/21
--------------------------

* Improved test;
* Continued on resolver (was named validate previously);

Version 0.0.1 - 2016/02/20
--------------------------

* First commit