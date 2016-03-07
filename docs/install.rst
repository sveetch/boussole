.. _virtualenv: http://www.virtualenv.org
.. _Pytest: http://pytest.org
.. _Napoleon: https://sphinxcontrib-napoleon.readthedocs.org
.. _Flake8: http://flake8.readthedocs.org

=======
Install
=======

::

    pip install boussole

It should be safe enough to install it on Linux, MacOSX and Windows until you 
have the right environment (needed devel libs, etc..).
    
Development
***********

For development there is some additional packages to install:

* `Pytest`_ for Unittests;
* Sphinx (using its `Napoleon`_ extension);
* `Flake8`_;

So use: ::

    pip install -r https://raw.githubusercontent.com/sveetch/boussole/master/dev_requirements.txt