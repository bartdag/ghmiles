'''
  Description of the module here.

  :copyright: Copyright 2011 Barthelemy Dagenais
  :license: BSD, see LICENSE for details
'''
from github2.client import Github
import re

MILESTONE_LABEL_V = re.compile(r'''^v\d+\.\d+$''')
'''Regex used to identify milestone labels of the form v0.1'''

MILESTONE_LABEL_NUM = re.compile(r'''^\d+\.\d+$''')
'''Regex used to identify numerical milestone labels of the form 0.1'''

class Milestone(object):

    def __init__(self, title, issues):
        self.title = title
        self.issues = issues
        self.total = len(issues)
        self.opened = sum((1 for issue in issues if issue.state == 'open'))
        self.closed = self.total - self.opened
        self.progress = float(self.closed) * 100.0 / float(self.total)

    def __repr__(self):
        return '<Milestone: {0}, {1} issues, {2:.2f}% completed>'.format(
                self.title, self.total, self.progress)

def get_milestone_labels(github, project, milestone_regex):
    labels = sorted(github.issues.list_labels(project), reverse=True)
    project_labels = (label for label in labels if milestone_regex.match(label))
    return project_labels

def get_milestone(github, project, milestone_label):
    issues = github.issues.list_by_label(project, milestone_label)
    return Milestone(milestone_label, issues)

def get_milestones(project, milestone_regex, as_list=False):
    '''Generates a list of milestones for a github project

    :param project: a string of the form `user/project`
    :param milestone_regex: a regular expression used to identify the labels
    representing milestones.
    '''
    github = Github()
    labels = get_milestone_labels(github, project, milestone_regex)
    milestones = (get_milestone(github, project, label) for
        label in labels) 

    if as_list:
        milestones = list(milestones)

    return milestones

