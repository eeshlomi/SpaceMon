#!/usr/bin/python

import unittest
from SpaceMon import spacemon, parseYml, mailMsg
from SpaceMon import main


class TestSpaceMon(unittest.TestCase):
    def test_spacemon(self):
        ''' Test that spacemon default, which is '.',
            returns higher than 0 free space: '''
        result = spacemon()['.']
        greaterThan = 0
        self.assertGreater(result, greaterThan)

    def test_spacemon_nopath(self):
        # Test OSError exception:
        result = spacemon(['nopath'])['nopath_path_not_found']
        equals = -1
        self.assertEqual(result, equals)

    def test_main(self):
        result = main({'threshold': 0,
                       'logfile': './test.log',
                       'disks': ['.'],
                       'mail': {'server': 'None',
                                'sender': 'mail-tester@xconnect.net',
                                'recipients': ['shlomir@xconnect.net']}
                       })
        equals = 0
        self.assertEqual(result, equals)

    def test_parseYml(self):
        result = parseYml('unittest.yml')
        equals = 0
        self.assertEqual(result, equals)

    def test_parseYml_nopath(self):
        # Test IOError exception:
        result = parseYml('nopath.yml')
        equals = 'config/log file access error'
        self.assertEqual(result, equals)

    def test_parseYml_bad_yml(self):
        # Test bad format:
        result = parseYml('2do.txt')
        equals = '2do.txt is not a valid yml file'
        self.assertEqual(result, equals)

    def test_parseYml_key_error(self):
        # Test KeyError:
        result = parseYml('unittest_missingKey.yml')
        equals = "The key 'threshold' is missing in unittest_missingKey.yml"
        self.assertEqual(result, equals)

    def test_parseYml_help(self):
        # Test --help:
        result = parseYml('--help')
        equals = 'Usage: SpaceMon.py [config-file]'
        self.assertEqual(result, equals)

    def test_parseYml_noarg(self):
        # Test unknown argunemt:
        result = parseYml('--unknown-argument')
        equals = 'unknown argument'
        self.assertEqual(result, equals)

    def test_mailMsg(self):
        result = mailMsg({'somepath': 89})
        equals = 0
        self.assertEqual(result, equals)

    def test_mailMsg_nopath(self):
        result = mailMsg({'nopath': -1})
        equals = 'could not access some disks'
        self.assertEqual(result, equals)

    def test_mailMsg_disk_alert(self):
        result = mailMsg({'somepath': 89}, 80)
        equals = 'disk usage alert'
        self.assertEqual(result, equals)


if __name__ == '__main__':
    unittest.main()
