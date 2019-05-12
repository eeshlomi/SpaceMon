#!/usr/bin/python

import unittest
from SpaceMon import spacemon, parseYml


class TestSpaceMon(unittest.TestCase):
    def test_spacemon(self):
        result = len(spacemon())
        expect = 1
        self.assertEqual(result, expect)

    def test_spacemon_nopath(self):
        result = len(spacemon(['nopath']))
        expect = 1
        self.assertEqual(result, expect)

    def test_parseYml(self):
        result = parseYml("unittest.yml")
        expect = 0
        self.assertEqual(result, expect)


if __name__ == '__main__':
    unittest.main()
