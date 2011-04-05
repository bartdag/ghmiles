'''
  ghmiles unit tests

  :copyright: Copyright 2011 Barthelemy Dagenais
  :license: BSD, see LICENSE for details
'''
from __future__ import unicode_literals
import unittest
import ghmiles

class TestMilestonesModel(unittest.TestCase):

    def test_key_label(self):
        self.assertEqual(ghmiles.label_key('1.0'),'00001.00000')
        self.assertEqual(ghmiles.label_key('12'),'00012')
        self.assertEqual(ghmiles.label_key('v3.35.67e-234b'),
                         'v00003.00035.00067e-00234b')

    def test_get_milestone_labels(self):
        labels = list(
          ghmiles.get_milestone_labels('bartdag/py4j', 
                                        ghmiles.MILESTONE_LABEL_V,
                                        False))

        self.assertTrue(len(labels) >= 7)
        self.assertEqual('v0.1',labels[0])
        self.assertEqual('v0.7',labels[6])

    def test_get_intel_milestone_labels(self):
        (project_labels, labels) = \
                ghmiles.get_intel_milestone_labels('bartdag/py4j', False)
        self.assertTrue(len(labels) > len(project_labels))
        self.assertTrue(len(project_labels) >= 7)
        self.assertEqual('v0.1',project_labels[0])
        self.assertEqual('v0.7',project_labels[6])

    def test_get_milestones(self):
        milestones = ghmiles.get_milestones('bartdag/py4j',
                ghmiles.MILESTONE_LABEL_V, False)
        milestone1 = milestones.next()
        self.assertEqual(milestone1.title, 'v0.1')
        self.assertAlmostEqual(milestone1.progress, 100.0)
        self.assertEqual(milestone1.total, 9)
        self.assertEqual(milestone1.opened, 0)
        issues_title = (issue.title for issue in milestone1.issues)
        self.assertTrue(u'Write a getting started tutorial' in issues_title)

    def test_get_milestones_without_regex(self):
        milestones = list(ghmiles.get_milestones('bartdag/py4j', 
            reverse=False))
        milestone1 = milestones[0]
        self.assertEqual(milestone1.title, 'v0.1')
        self.assertAlmostEqual(milestone1.progress, 100.0)
        self.assertEqual(milestone1.total, 9)
        self.assertEqual(milestone1.opened, 0)
        issues_title = (issue.title for issue in milestone1.issues)
        self.assertTrue(u'Write a getting started tutorial' in issues_title)
        self.assertTrue(len(milestones) >= 7)

    def test_get_milestones_from_labels(self):
        milestones = list(ghmiles.get_milestones_from_labels('bartdag/py4j',
                ['v0.2','v0.4']))
        self.assertEqual(milestones[0].total, 12)
        self.assertEqual(milestones[1].total, 14)

    def test_get_simple_html_page(self):
        milestones = list(ghmiles.get_milestones_from_labels('bartdag/py4j',
                ['v0.2','v0.1']))
        html = ghmiles.get_simple_html_page(milestones, 'Py4J')
        self.assertTrue(html.startswith('<!DOCTYPE html PUBLIC'))
        self.assertTrue(html.endswith('</html>'))

    def test_get_intel_milestones_tag(self):
        (project_labels, labels) = \
                ghmiles.get_intel_milestone_labels('bartdag/py4j', False,
                        None, ghmiles.tags_get, ghmiles.tags_key, 
                        ghmiles.tags_sort_key)
        self.assertTrue(len(project_labels) >= 6)
        self.assertEqual('0.1', project_labels[0][0])

    def test_get_milestone_from_tag(self):
        (project_labels, labels) = \
                ghmiles.get_intel_milestone_labels('bartdag/py4j', False,
                        None, ghmiles.tags_get, ghmiles.tags_key, 
                        ghmiles.tags_sort_key)
        tag1 = ghmiles.get_complete_tag('bartdag/py4j', project_labels[0])
        tag2 = ghmiles.get_complete_tag('bartdag/py4j', project_labels[1])
        taglast = ghmiles.get_complete_tag('bartdag/py4j', project_labels[-1])

        issues = ghmiles.get_all_issues('bartdag/py4j')
        m1 = ghmiles.get_milestone_from_tag('bartdag/py4j', None, tag1, issues)
        m2 = ghmiles.get_milestone_from_tag('bartdag/py4j', tag1, tag2, issues)
        mlast = ghmiles.get_milestone_from_tag('bartdag/py4j', taglast,
                None, issues)
        
        # Because the timestamp is off: tickets were imported from Trac!
        self.assertEqual(0, m1.total)
        self.assertEqual(0, m2.total)
        # Reasonable boundaries
        self.assertTrue(mlast.total > 0 and mlast.total < 20)

    def test_get_milestones_from_tags(self):
        milestones = list(ghmiles.get_milestones('bartdag/py4j',
                milestone_type=ghmiles.BY_TAG))
        self.assertTrue(len(milestones) >= 7)
        self.assertTrue(milestones[0].total > 0 and milestones[0].total < 20)
        self.assertEqual('current', milestones[0].title)
        self.assertEqual('0.1', milestones[-1].title)
        
        milestones = list(ghmiles.get_milestones('bartdag/py4j',
                reverse=False, milestone_type=ghmiles.BY_TAG))
        self.assertTrue(len(milestones) >= 7)
        self.assertTrue(milestones[-1].total > 0 and milestones[-1].total < 20)
        self.assertEqual('0.1', milestones[0].title)
        self.assertEqual('current', milestones[-1].title)
        
if __name__ == '__main__':
    unittest.main()
