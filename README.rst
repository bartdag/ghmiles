ghmiles - Github Milestone Generator
====================================

:Authors:
  Barthelemy Dagenais
:Version: 0.1

This is a Python library that generates a milestone model from the issues of a
github repository. The library also generates a roadmap inspired by `Trac`_.
See the `Py4J Roadmap`_ for an example.

.. _`Trac`: http://trac.edgewall.org/
.. _`Py4J Roadmap`: http://py4j.sourceforge.net/py4j_fancy_roadmap.html


Introduction
------------

GitHub provides an issue tracker with each repository, but unfortunately, it
does not offer a way to track the progress of milestones (or versions) beside
listing all issues that are closed or open. 

ghmiles is a Python library that generates a milestone model from the issues in
a GitHub repository. ghmiles can optionaly generate an HTML page similar to a
`Trac roadmap`_. See the `Py4J Roadmap`_ for an example of a generated roadmap.

A milestone is a list of issues having the same label. The progress of a
milestone is obtained by dividing the number of closed issues by the number of
total issues. 

Users of ghmiles can specify which labels identify a milestone by providing a
regular expression. 

.. _`Trac roadmap`: http://trac.edgewall.org/roadmap
.. _`Py4J Roadmap`: http://py4j.sourceforge.net/py4j_fancy_roadmap.html

Installation
------------

The best way to install ghmiles is to use `pip`_ (or setuptools or distribute):

::

  $ pip install ghmiles 
  
This will install ghmiles and python-github2.

.. _`pip`: http://pypi.python.org/pypi/pip

Generating a Milestone Model
----------------------------

To get a list of milestones from a GitHub project:

::

  >>> import ghmiles
  >>> milestones = ghmiles.get_milestones(project='bartdag/py4j',milestone_regex=ghmiles.MILESTONE_LABEL_V)
  >>> milestone = milestones.next()                                                                                                                                 
  >>> milestone.title                                                                                                                                               
  u'v0.7'                                                                                                                                                           
  >>> milestone.total                                                                                                                                               
  7                                                                                                                                                                 
  >>> milestone.closed                                                                                                                                              
  0                                                                                                                                                                 
  >>> milestone.opened                                                                                                                                              
  7                                                                                                                                                                 
  >>> milestone.progress                                                                                                                                            
  0.0                                                                                                                                                               
  >>> milestone.issues[0]                                                                                                                                           
  <Issue: Better unit test organization for Py4J-Python>                                                                                                            
  >>> milestone.issues[0].title                                                                                                                                     
  u'Better unit test organization for Py4J-Python'

The ``milestones`` variable is actually an iterator. Each time ``next()`` is
called, a request is made to GitHub to retrieve all issues pertaining to this
milestone. The issues are of type ``github2.issues.Issue``. 

The milestone_regex is a regular expression used to determine whether a label
is a milestone. ghmiles provide two regular expressions:

* ``ghmiles.MILESTONE_LABEL_V`` recognizes labels of the form ``vX.X`` where X is a
  number.

* ``ghmiles.MILESTONE_LABEL_NUM`` recognizes labels of the form ``X.X`` where X is a
  number.

Other interesting functions:

::

  >>> labels = ghmiles.get_milestone_labels('bartdag/py4j', ghmiles.MILESTONE_LABEL_V)                                                                       
  >>> list(labels)                                                                                                                                                        
  [u'v0.7', u'v0.6', u'v0.5', u'v0.4', u'v0.3', u'v0.2', u'v0.1']
  >>> milestones = ghmiles.get_milestones_from_labels('bartdag/py4j', labels[-1:])                                                                         
  >>> milestones.next()                                                                                                                                            
  <Milestone: v0.1, 9 issues, 100.00% completed>  


Generating a Roadmap HTML Page
------------------------------

To generate a simple roadmap such as `this one
<http://py4j.sourceforge.net/py4j_simple_roadmap.html>`_:

::

  >>> milestones = ghmiles.get_milestones('bartdag/py4j', ghmiles.MILESTONE_LABEL_V)                                                                                
  >>> ghmiles.get_simple_html_page(milestones=milestones, project_name='Py4J', save_path='simple_roadmap.html')

To generate a fancy roadmap such as `this one
<http://py4j.sourceforge.net/py4j_fancy_roadmap.html>`_:

::

  >>> milestones = ghmiles.get_milestones('bartdag/py4j', ghmiles.MILESTONE_LABEL_V)                               
  >>> ghmiles.get_fancy_html_page(milestones=milestones, project='bartdag/py4j', project_name='Py4J', save_path='fancy_roadmap.html') 

License
-------

This software is licensed under the ``New BSD License``. See the ``LICENSE``
file in the top distribution directory for the full license text.
