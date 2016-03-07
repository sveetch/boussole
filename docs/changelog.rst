
=========
Changelog
=========

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