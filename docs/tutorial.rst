.. _virtualenv: http://www.virtualenv.org
.. _pip: https://pip.pypa.io
.. _Pytest: http://pytest.org
.. _Napoleon: https://sphinxcontrib-napoleon.readthedocs.org
.. _Flake8: http://flake8.readthedocs.org

========
Tutorial
========

Once Boussole is correctly installed, you will be able to start a project to work on.

#. Go to a directory where you want to start a new project then execute command: ::

    boussole startproject
#. Answer to the questions (let the default values for this sample): ::

    Project base directory [.]:
    Settings file name [settings.json]:
    Sources directory [scss]:
    Target directory [css]:
#. Write some SASS file into ``scss`` directory;
#. From your SASS project directory (where belong the ``settings.json`` file) just execute command: ::

    boussole compile
#. And voila, your valid SASS files should have been compiled to the ``css`` directory;
