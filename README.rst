.. _Watchdog: https://github.com/gorakhargosh/watchdog

========
Boussole
========

Aims to reproduce the useful Compass commandline tool behavior for 'build' and 'watch' actions.

This is under construction, not even an Alpha for now.

Requires
********

* `Watchdog`_ == 0.8.3;

Install
*******

First install the package ::

    pip install boussole

TODO
****

* Finish API;

  * [x] SCSS parser for import rules;
  * [x] Path resolving through scss project and libraries;
  * [x] Project inspector to find import dependancies;
  * [ ] Finish API;
  * [x] unittests on API;
  * [ ] Documentation coverage on API;
  
    * Docstring for arguments and module/class descriptions;
    * Renaming unittests test case;
    * Clean every debug pointers;

* Commandline interface;
