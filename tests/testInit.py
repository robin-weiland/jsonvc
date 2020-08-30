#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__date__ = "2020-08-30"
__version__ = "0.0.0"

__all__ = ()

from os.path import exists
import jsonvc
import jsonvc.tools
from json import loads
from pyfakefs.fake_filesystem_unittest import TestCase


class InitTest(TestCase):
    def setUp(self) -> None:
        self.setUpPyfakefs(modules_to_reload=[jsonvc, jsonvc.tools])

    def test_init(self):
        self.assertFalse(exists('test.py'))
        jsonvc.JSONVC('test.py')
        self.assertTrue(exists('test.py'))

        self.assertEqual(
            loads("[]"),
            jsonvc.tools.load('test.py')
        )


if __name__ == '__main__': pass
