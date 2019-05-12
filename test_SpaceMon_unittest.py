#!/usr/bin/python

import unittest
from SpaceMon import spacemon, parseYml


class TestSpaceMon(unittest.TestCase):
    def test_spacemon(self):
        result = spacemon()['.']
        greaterThan = 0
        self.assertGreater(result, greaterThan)

    def test_spacemon_nopath(self):
        result = spacemon(['nopath'])['nopath_path_not_found']
        equals = -1
        self.assertEqual(result, equals)

    def test_parseYml(self):
        result = parseYml("unittest.yml")
        equals = 0
        self.assertEqual(result, equals)


if __name__ == '__main__':
    unittest.main()
