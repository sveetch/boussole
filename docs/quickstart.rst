.. _virtualenv: http://www.virtualenv.org
.. _pip: https://pip.pypa.io
.. _Pytest: http://pytest.org
.. _Napoleon: https://sphinxcontrib-napoleon.readthedocs.org
.. _Flake8: http://flake8.readthedocs.org

===========
Quick start
===========

Once Boussole is correctly installed, you will be able to start a project to
work on.

#. Go to a directory where you want to start a new project then execute
   command: ::

    boussole startproject
#. Answer to the questions (let the default values for this sample): ::

    Project base directory [.]:
    Sources directory [scss]:
    Target directory [css]:
    Settings format name (json, yaml) [json]:
#. Write some Sass files into ``scss`` directory;
#. From your new Sass project directory (where belong the ``boussole.json``
   file) just execute command: ::

    boussole compile
#. And voila, your valid Sass files should have been compiled to the ``css``
   directory;
