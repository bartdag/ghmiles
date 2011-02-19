#!/usr/bin/env python

'''
  Description of the module here.

  :copyright: Copyright 2011 Barthelemy Dagenais
  :license: BSD, see LICENSE for details
'''

from distutils.core import setup

setup(name='ghmiles',
      version='0.1',
      description='GitHub Milestones',
      long_description=
      '''
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
''',
      author='Barthelemy Dagenais',
      author_email='barthe@users.sourceforge.net',
      license='BSD License',
      url='https://github.com/bartdag/ghmiles',
      py_modules=['ghmiles']
     ) 
