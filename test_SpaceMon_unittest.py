#!/usr/bin/python

import unittest
from SpaceMon import yaml_run


class TestSpaceMon(unittest.TestCase):
    def test_yaml_run(self):
        result = yaml_run("unittest.yml")
        expect = 0
        self.assertEqual(result, expect)


if __name__ == '__main__':
    unittest.main()
