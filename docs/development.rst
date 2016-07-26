.. _virtualenv: http://www.virtualenv.org
.. _pip: https://pip.pypa.io
.. _Pytest: http://pytest.org
.. _Napoleon: https://sphinxcontrib-napoleon.readthedocs.org
.. _Flake8: http://flake8.readthedocs.org
.. _Sphinx: http://www.sphinx-doc.org
.. _tox: http://tox.readthedocs.io

===========
Development
===========

Development requirement
***********************

Boussole is developed with:

* *Test Development Driven* (TDD) using `Pytest`_;
* Respecting flake and pip8 rules using `Flake8`_;
* `Sphinx`_ for documentation with enabled `Napoleon`_ extension (using only the *Google style*);

Every requirement is available in file ``dev_requirements.txt``.

Install for development
***********************

First ensure you have `pip`_ and `virtualenv`_ installed, then type this: ::

    mkdir Boussole-dev
    cd Boussole-dev
    virtualenv .
    git clone https://github.com/sveetch/boussole.git
    bin/pip install -e boussole
    bin/pip install -r boussole/requirements/dev.txt
    source bin/activate

Boussole will be installed in editable mode from the last commit on master branch.

When it's done, you will be able to check for boussole version, just type: ::

    boussole version

Unittests
---------

Unittests are made to works on `Pytest`_, a shortcut in Makefile is available to start them on your current development install: ::

    make tests

