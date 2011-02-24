'''
  ghmiles unit tests

  :copyright: Copyright 2011 Barthelemy Dagenais
  :license: BSD, see LICENSE for details
'''

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
        labels = ghmiles.get_intel_milestone_labels('bartdag/py4j', False)
        self.assertTrue(len(labels) >= 7)
        self.assertEqual('v0.1',labels[0])
        self.assertEqual('v0.7',labels[6])

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


        
if __name__ == '__main__':
    unittest.main()
