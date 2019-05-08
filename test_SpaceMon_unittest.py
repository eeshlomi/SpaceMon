#!/usr/bin/python

import unittest
from SpaceMon import main, yaml_run


class TestSpaceMon(unittest.TestCase):
    def test_main(self):
        result = len(main(["recipient@domain.com"]))
        expect = 1
        self.assertEqual(result, expect)

    def test_yaml_run(self):
        result = len(yaml_run("unittest.yml"))
        expect = 1
        self.assertEqual(result, expect)


if __name__ == '__main__':
    unittest.main()
