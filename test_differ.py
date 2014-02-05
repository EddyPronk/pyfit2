import unittest
from plaintypes import Cell
from differ import Differ
from engines import Engine

def compare(e,c):
    return e == c

class TestDiffer(unittest.TestCase):

    def test_two_rows_with_difference(self):
        '''See fitbook Figure 5.3'''
        computed = [['anna', 'lotr'],
                    ['luke', 'lotr']]
        expected = [[Cell('anna'), Cell('shrek')],
                    [Cell('luke'), Cell('lotr')]]
        
        cell = expected[0][1]
        desc = [str ,str]
        #differ = Differ(compare, desc)
        differ = Differ(compare, desc)
        differ.match(expected, computed, 0)
        cell = expected[0][1]
        #print 'missing : %s' % differ.missing
        #print 'surplus : %s' % differ.surplus
        #print expected
        self.assertEqual(cell.expected, 'shrek')
        # fixme
        #self.assertEqual(cell.actual,   'lotr')
        #print cell.__dict__

    def test_one_missing_row(self):
        computed = [['anna', 'lotr']]
        expected = [['anna', 'shrek'],
                    ['luke', 'lotr']]
        
        differ = Differ(compare, [ str, str ])
        differ.match(expected, computed, 0)
        self.assertEqual(differ.missing, [['luke', 'lotr']])
        self.assertEqual(differ.surplus, [])

    def test_one_surplus_row(self):
        computed = [['anna', 'lotr'],
                    ['luke', 'lotr']]
        expected = [['anna', 'shrek']]
        
        differ = Differ(compare, [str,str])
        differ.match(expected, computed, 0)
        self.assertEqual(differ.missing, [])
        self.assertEqual(differ.surplus, [['luke', 'lotr']])
