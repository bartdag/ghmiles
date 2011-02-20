''' 
  ghmiles generates a milestones model from the list of issues in a github
  repository. 

  :copyright: Copyright 2011 Barthelemy Dagenais
  :license: BSD, see LICENSE for details
'''
from github2.issues import Issues, Issue
from github2.client import Github
import datetime
import StringIO
import re

#### MONKEY PATCH github2 ####

def list_by_label(self, project, label):
    """Get all issues for project' with label'.

    ``project`` is a string with the project owner username and repository
    name separated by ``/`` (e.g. ``ask/pygithub2``).
    ``label`` is a string representing a label (e.g., ``bug``).
    """
    return self.get_values("list", project, "label", label, filter="issues",
                           datatype=Issue)

def list_labels(self, project):
    """Get all labels for project'.

    ``project`` is a string with the project owner username and repository
    name separated by ``/`` (e.g. ``ask/pygithub2``).
    """
    return self.get_values("labels", project, filter="labels")

Issues.list_by_label = list_by_label
Issues.list_labels = list_labels


#### CONSTANTS ####

MILESTONE_LABEL_V = re.compile(r'''^v\d+\.\d+$''')
'''Regex used to identify milestone labels of the form v0.1'''

MILESTONE_LABEL_NUM = re.compile(r'''^\d+\.\d+$''')
'''Regex used to identify numerical milestone labels of the form 0.1'''

SIMPLE_HTML_HEADER = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <title>{0} Roadmap</title>
  </head>
  <body>
    <h1>{0} Roadmap</h1>
'''

SIMPLE_HTML_FOOTER = '''
  <hr/>
  <p>
  Generated by <a href="https://github.com/bartdag/ghmiles">ghmiles</a>
  on {0}.
  </p>
  <p>
    <a href="http://validator.w3.org/check?uri=referer"><img
        src="http://www.w3.org/Icons/valid-xhtml10"
        alt="Valid XHTML 1.0 Strict" height="31" width="88" /></a>
  </p>
  </body>
</html>'''

FANCY_HTML_HEADER = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
  <head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <title>{0} Roadmap</title>
  <link type="text/css" rel="stylesheet" href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.9/themes/ui-lightness/jquery-ui.css"/>
  <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.5.0/jquery.min.js"></script>
  <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.9/jquery-ui.min.js"></script>
  <script type="text/javascript">
    $(function() {{
      $(".details").click(function(e) {{
        $(e.target).parent().next().toggle("blind", {{}}, 500);
      }});
    }});
  </script>
  <style type="text/css">
  #doc {{
    margin:auto;
    width: 960px;
    font-family: Futura, "Century Gothic", AppleGothic, sans-serif;
  }}
 
  h1 {{
    color: #1049A9;
  }}

  h2 {{
    color: #1049A9;
    margin-top: 50px;
  }}

  a {{
    color: #A65100;
  }}

  a:hover {{
    color: #1049A9;
  }}

  .pb {{
    width: 480px;
    font-size: 50%;
  }}

  .pb_label {{
    float: right;
    font-size: 200%;
    font-weight: bold;
  }}

  .issues_list {{
    list-style-type: none;
    display: none;
  }}

  .issues_list li a {{
    font-weight: bold;
  }}

  .tickets {{
    font-size: 0.7em;
    font-style: italic;
  }}
  
  .tickets dt {{
    display: inline;
    margin-left: 1em;
  }}

  .tickets dd {{
    display: inline;
    margin: 0 1.5em 0 0.5em;
  }}

  #hd, #ft {{
    height: 40px;
  }}

  #ft {{
    border-top: 1px solid #ccc;
  }}

  #hd {{
    text-align: center;
  }}
  </style>
  </head>
  <body id="doc">
    <div id="hd">
      <h1>{0} Roadmap</h1>
    </div>
    <div id="main">
'''

FANCY_HTML_FOOTER = '''
    </div>
    <div id="ft">
    <p>
    Generated by <a href="https://github.com/bartdag/ghmiles">ghmiles</a>
    on {0}.
    </p>
    <p>
    <a href="http://validator.w3.org/check?uri=referer"><img
        src="http://www.w3.org/Icons/valid-xhtml10"
        alt="Valid XHTML 1.0 Strict" height="31" width="88" /></a>
    </p>
    </div>
  </body>
</html>'''

#### MILESTONE MODEL #####

class Milestone(object):

    def __init__(self, title, issues):
        self.title = title
        self.issues = issues
        self.issues.sort(key=lambda item: int(item.number))
        self.total = len(issues)
        self.opened = sum((1 for issue in issues if issue.state == 'open'))
        self.closed = self.total - self.opened
        self.progress = float(self.closed) * 100.0 / float(self.total)

    def __repr__(self):
        return '<Milestone: {0}, {1} issues, {2:.2f}% completed>'.format(
                self.title, self.total, self.progress)

def label_key(label, padding=5):
    '''Returns a padded key from a label representing a milestone number.
    All parts of a label that are numbers are padded so that alphabetical
    sorting can work as expected (e.g., '2.0' < '11.0'). 

    For example, this function will return 'v00001.00022e-00123b' if label =
    'v1.22e-123b'.

    :param label: the milestone label
    :param padding: the maximum number of characters for each numeric part.
           Default=5
    :return: a key that can be used in alphabetical sorting
    '''
    key = prefix = ''
    components = []
   
    in_prefix = True
    current_number = current_suffix = ''

    for c in label:
        if not c.isdigit():
            if in_prefix:
                prefix += c
            else:
                current_suffix += c
        else:
            if in_prefix:
                in_prefix = False
            if current_suffix != '':
                components.append((current_number, current_suffix))
                current_number = current_suffix = ''
            current_number += c

    if not in_prefix and current_number != '':
        components.append((current_number, current_suffix))

    key = prefix
    for component in components:
        key += component[0].rjust(padding,'0') + component[1]

    return key

def get_milestone_labels(project, milestone_regex, reverse=True, github=None):
    if github is None:
        github = Github(requests_per_second=1)
    labels = sorted(github.issues.list_labels(project), key=label_key, reverse=reverse)
    project_labels = (label for label in labels if milestone_regex.match(label))
    return project_labels

def get_milestone(project, milestone_label, github=None):
    if github is None:
        github = Github(requests_per_second=1)
    issues = github.issues.list_by_label(project, milestone_label)
    return Milestone(milestone_label, issues)

def get_milestones(project, milestone_regex, reverse=True):
    '''Generates a list of milestones for a github project

    :param project: a string of the form `user/project`
    :param milestone_regex: a regular expression used to identify the labels
           representing milestones.
    :param reverse: If True (default), sort the milestones from the highest 
           number to the lowest. Oppositive if False.
    :return: A generator (iterator) of milestones. 
    '''

    github = Github(requests_per_second=1)
    labels = get_milestone_labels(project, milestone_regex, reverse, github)
    milestones = (get_milestone(project, label, github) for
        label in labels) 

    return milestones

def get_milestones_from_labels(project, labels):
    '''Generates a list of milestones from the specified issue labels of a 
    github project. This can be used to generate a milestone model for recent
    milestones only.

    :param project: a string of the form `user/project`
    :param labels: a list of labels used to generate milestones. 
    :return: A generator (iterator) of milestones. 
    '''
    github = Github(requests_per_second=1)
    milestones = (get_milestone(project, label, github) for
        label in labels) 

    return milestones


#### HTML GENERATION ####

def write_simple_html_milestones(milestones, output):
    for milestone in milestones:
        output.write('<h2>Milestone: {0}</h2>\n'.format(milestone.title))
        output.write('<p><strong>Progress: {0}%</strong></p>'
                .format(milestone.progress))
        output.write('<p><em>Number of tickets: ')
        output.write('closed: {0} active: {1} total: {2}</em></p>\n'
                .format(milestone.closed, milestone.opened, milestone.total))
        output.write('<p>Issues:</p>\n<ul>\n')
        for issue in milestone.issues:
            output.write('<li> #{0} {1} <em>{2}</em></li>\n'
                    .format(issue.number, issue.title, issue.state))
        output.write('</ul>\n')

def get_simple_html_page(milestones, project_name = 'GitHub Project', 
        save_path=None, header=SIMPLE_HTML_HEADER, footer=SIMPLE_HTML_FOOTER):
    '''Generates a simple HTML page similar to a Trac roadmap.

    :param milestones: a list (or iterator) of milestones.
    :param project_name: a human-readable project name. (optional)
    :param save_path: the output path used to save the HTML page. If None, a
           string containing the HTML page will be returned instead.
    :param header: the HTML header used to generate the HTML page. (optional)
    :param footer: the HTML footer used to generate the HTML page. (optional)
    :return: None if a save_path is provided, an HTML string otherwise.
    '''

    return_value = None

    if save_path is None:
        output = StringIO.StringIO()
    else:
        output = open(save_path, 'w')

    output.write(header.format(project_name))

    write_simple_html_milestones(milestones, output)

    output.write(footer.format(str(datetime.datetime.now())))

    if save_path is None:
        return_value = output.getvalue()

    output.close()

    return return_value


def write_fancy_html_milestones(milestones, project, output):
    for milestone in milestones:
        new_title = milestone.title.replace('.','--')
        progress = int(milestone.progress)

        output.write('<a name="{0}"></a>'.format(milestone.title))
        output.write('<h2>Milestone: {0}</h2>\n'.format(milestone.title))
        output.write('''
        <script type="text/javascript">
        $(function() {{
          $("#progressbar{0}").progressbar({{value: {1} }});
          }});
        </script>
        '''.format(new_title,progress))
        output.write('''
        <div class="pb">
        <div id="progressbar{0}"></div>
        <div class="pb_label">{1}%</div>
        </div>
        '''.format(new_title, progress))
        output.write('''
        <dl class="tickets">
          <dt>Number of tickets:</dt><dd></dd>
          <dt>closed:</dt>
          <dd>{0}</dd>
          <dt>active:</dt>
          <dd>{1}</dd>
          <dt>total:</dt>
          <dd>{2}</dd>
        </dl>
        '''.format(milestone.closed, milestone.opened, milestone.total))
        output.write('<p><a href="#{0}" class="details">'
                .format(milestone.title))
        output.write('List of Issues:</a></p>\n')
        output.write('<ul class="issues_list">\n')
        for issue in milestone.issues:
            output.write(
                    '<li><a href="https://github.com/{0}/issues/{1}">#{1}</a>'
                    .format(project, issue.number))
            output.write(' {0}'.format(issue.title))
            output.write(' <strong>- {0}</strong></li>\n'.format(issue.state))
        output.write('</ul>\n')

def get_fancy_html_page(milestones, project, project_name = None,
        save_path=None, header=FANCY_HTML_HEADER, footer=FANCY_HTML_FOOTER):
    '''Generates a fancy HTML page similar to a Trac roadmap.

    :param milestones: a list (or iterator) of milestones.
    :param project: a string of the form `user/project`
    :param project_name: a human-readable project name. (optional)
    :param save_path: the output path used to save the HTML page. If None, a
           string containing the HTML page will be returned instead.
    :param header: the HTML header used to generate the HTML page. (optional)
    :param footer: the HTML footer used to generate the HTML page. (optional)
    :return: None if a save_path is provided, an HTML string otherwise.
    '''

    return_value = None

    if project_name is None:
        project_name = project.split('/')[1]

    if save_path is None:
        output = StringIO.StringIO()
    else:
        output = open(save_path, 'w')

    output.write(header.format(project_name))

    write_fancy_html_milestones(milestones, project, output)

    output.write(footer.format(str(datetime.datetime.now())))

    if save_path is None:
        return_value = output.getvalue()

    output.close()

    return return_value


