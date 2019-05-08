#!/usr/bin/python

import unittest
from SpaceMon import spacemon, main


class TestSpaceMon(unittest.TestCase):
    def test_spacemon(self):
        result = len(spacemon(["."]))
        expect = 1
        self.assertEqual(result, expect)

    def test_main(self):
        result = main("unittest.yml")
        expect = 0
        self.assertEqual(result, expect)


if __name__ == '__main__':
    unittest.main()
