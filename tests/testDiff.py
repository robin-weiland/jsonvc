#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2020-08-30"
__version__ = "0.0.0"

__all__ = ()

from jsonvc.diffs import Diff
from unittest import TestCase


class DiffTest(TestCase):
    def test_merge(self):
        diff1 = Diff()
        diff2 = Diff(dict(a=1, b=2), {'c'})
        diff3 = Diff(dict(a=4), {'b'})
        diff2and3 = Diff(dict(a=4), {'b', 'c'})

        diff1.merge(diff2)

        self.assertEqual(
            diff1,
            diff2,
        )

        diff2.merge(diff3)

        self.assertEqual(
            diff2and3,
            diff2
        )

    def test_len(self):
        self.assertEqual(
            0,
            len(Diff()),
            'Empty Diff was not of length 0!'
        )
        self.assertEqual(
            1,
            len(Diff(changes=dict(a=1))),
            'Diff with one was not of length 1!'
        )
        self.assertEqual(
            30,
            len(Diff(deletions=set(i for i in range(30)))),
            'Diff with 30 deletions was not of length 30!'
        )
        self.assertEqual(
            10,
            len(Diff(changes=dict((str(i), i,) for i in range(5)), deletions=set(i for i in range(5)))),
            'Diff with 5 changes and 5 deletions was not of length 10!'
        )

    def test_bool(self):
        self.assertFalse(
            Diff(),
            'Empty Diff should be False!'
        )
        self.assertTrue(
            Diff(changes=dict((str(i), i,) for i in range(5)), deletions=set(i for i in range(5))),
            'Non-Empty Diff should be True!'
        )

    def test_reset(self):
        diff = Diff(changes=dict((str(i), i,) for i in range(5)), deletions=set(i for i in range(5)))
        self.assertTrue(diff)
        diff.reset()
        self.assertFalse(diff)

    def test_setitem(self):
        diff = Diff()
        self.assertFalse(diff)
        diff['a'] = 1
        self.assertTrue(diff)
        self.assertEqual(
            dict(a=1),
            diff.changes
        )
        self.assertFalse(diff.deletions)

    def test_delitem(self):
        diff = Diff()
        self.assertFalse(diff)
        diff['a'] = 1
        diff['b'] = 3
        self.assertTrue(diff)
        del diff['b']
        self.assertEqual(
            Diff(changes=dict(a=1), deletions={'b'}),
            diff
        )
        self.assertTrue(diff)

    def test_update(self): pass
    # diff = Diff()
    # self.assertFalse(diff)
    # diff.update(dict(a=1, b=2, c=3), dict(d=4))
    # self.assertTrue(diff)
    # self.assertEqual(
    #     Diff(changes=dict(d=4)),
    #     diff
    # )

    def test_pop(self):
        diff = Diff()
        self.assertFalse(diff)
        diff['a'] = 1
        diff['b'] = 2
        diff['c'] = 3
        self.assertTrue(diff)
        diff.pop('c')
        self.assertEqual(
            Diff(dict(a=1, b=2), {'c'}),
            diff
        )

    def test_setdefault(self):
        diff = Diff()
        self.assertFalse(diff)
        diff['a'] = 1
        diff['b'] = 2
        diff['c'] = 3
        diff.setdefault('a', 4)
        self.assertEqual(
            Diff(dict(a=1, b=2, c=3)),
            diff
        )
        diff.setdefault('d', 4)
        self.assertEqual(
            Diff(dict(a=1, b=2, c=3, d=4)),
            diff
        )

    def test_clear(self):
        diff = Diff()
        self.assertFalse(diff)
        diff['a'] = 1
        diff['b'] = 1
        diff['c'] = 1
        self.assertTrue(diff)
        diff.clear(('a', 'b', 'c',))
        self.assertEqual(
            {'a', 'b', 'c'},
            diff.deletions
        )
        self.assertFalse(diff.changes)


if __name__ == '__main__': pass
