ghmiles - Github Milestone Generator
====================================

:Authors:
  Barthelemy Dagenais
:Version: 0.1

This is a Python library that generates a milestone model from the issues of a
github repository. The milestone model is inspired by `Trac`_ roadmap.

.. _`Trac`: http://trac.edgewall.org/

Introduction
------------

GitHub provides an issue tracker with each repository, but unfortunately, it
does not offer a way to track the progress of milestones (or versions) beside
seing the issues that are closed or open. 

ghmiles is a Python library that generates a milestone model from the issues in
a GitHub repository. ghmiles can optionaly generate an HTML page similar to a
`Trac roadmap`_. It can also pass the milestone model to a `Jinja`_ template.

A milestone is a list of issues having the same label. The progress of a
milestone is obtained by dividing the number of closed issues by the number of
total issues. 

Users of ghmiles can specify which labels identify a milestone by providing a
regular expression. 

.. _`Trac roadmap`: http://trac.edgewall.org/roadmap
.. _`Jinja`: http://jinja.pocoo.org/ 

Installation
------------

The best way to install ghmiles is to use the requirements file with `pip`_:

  pip install -r https://github.com/bartdag/ghmiles/raw/master/requirements.txt
  
This will install ghmiles and a patched version of python-github2 from github
repositories. As soon as Bart's patch is integrated into python-github2,
ghmiles will be available on pypi.

To uninstall ghmiles and github2, just use pip:
  
  pip uninstall ghmiles

  pip uninstall github2
  
  rm -rf $PATH_TO_VIRTUALENV/src/ghmiles
  
  rm -rf $PATH_TO_VIRTUALENV/src/github2

The last two steps are required if you want to reinstall or upgrade ghmiles.

.. _`pip`: http://pypi.python.org/pypi/pip

Generating Milestone Model
--------------------------

TBD

Generating HTML Page
--------------------

TBD

Generating Jinja Template
-------------------------

TBD

License
-------

This software is licensed under the ``New BSD License``. See the ``LICENSE``
file in the top distribution directory for the full license text.
