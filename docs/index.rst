.. Boussole documentation master file, created by
   sphinx-quickstart on Sun Mar  6 12:12:38 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.
   
.. _virtualenv: http://www.virtualenv.org/
.. _Compass: http://compass-style.org/
.. _Watchdog: https://github.com/gorakhargosh/watchdog
.. _click: http://click.pocoo.org/6/

Welcome to Boussole's documentation!
====================================

Aims to reproduce the useful Compass commandline tool behavior for 'build' and 'watch' actions.

This is under construction, not even an Alpha for now.

Links
*****

* Read the documentation on `Read the docs <http://boussole.readthedocs.org/>`_;
* Download its `PyPi package <http://pypi.python.org/pypi/boussole>`_;
* Clone it on its `Github repository <https://github.com/sveetch/boussole>`_;

Requires
********

* `Watchdog`_ == 0.8.3;
* `click`_ == 6.2;

TODO
****

* [ ] Finish API;

  * [x] SCSS parser for import rules;
  * [x] Path resolving through scss project and libraries;
  * [x] Project inspector to find import dependancies;
  * [x] Finish API;
  * [x] unittests on API;
  * [x] Documentation coverage on API;
  
    * [x] Docstring for arguments and module/class descriptions;
    * [ ] Renaming unittests test case;
    * [x] Clean every debug pointers;
    * [x] Pass Flake8 validation;

* [ ] Commandline interface;

Table of contents
*****************

.. toctree::
   :maxdepth: 2

   install.rst
   api.rst
   changelog.rst
