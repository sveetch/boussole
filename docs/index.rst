.. Boussole documentation master file, created by
   sphinx-quickstart on Sun Mar  6 12:12:38 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _virtualenv: http://www.virtualenv.org/
.. _Compass: http://compass-style.org/
.. _Watchdog: https://github.com/gorakhargosh/watchdog
.. _click: http://click.pocoo.org/5/
.. _libsass: https://github.com/dahlia/libsass-python

Welcome to Boussole's documentation!
====================================

This is a commandline interface to build SASS projects using `libsass`_.

Alike the Compass commandline, there is 'build' and 'watch' actions to build all SASS files.

.. Warning::
    This is under construction, almost an Alpha for now.

.. Note::
    Old SASS syntax (the *indented syntax*) is not totally supported and actually this is not really planned to do it.

Links
*****

* Read the documentation on `Read the docs <http://boussole.readthedocs.org/>`_;
* Download its `PyPi package <http://pypi.python.org/pypi/boussole>`_;
* Clone it on its `Github repository <https://github.com/sveetch/boussole>`_;

Requires
********

* `Watchdog`_ == 0.8.3;
* `click`_ == 5.1;
* `libsass`_ == 0.11.0;

User’s Guide
************

.. toctree::
   :maxdepth: 2

   install.rst
   changelog.rst
   api/index.rst
