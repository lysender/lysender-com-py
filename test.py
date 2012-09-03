#!/usr/bin/python
import optparse
import sys
# Install the Python unittest package before you run this script.
import unittest

USAGE = """%prog SDK_PATH TEST_PATH
Run unit tests for App Engine apps.

SDK_PATH    Path to the SDK installation
TEST_PATH   Path to package containing test modules
PATTERN     File name patter for test modules"""


def main(sdk_path, test_path, test_pattern):
    sys.path.insert(0, sdk_path)
    import dev_appserver
    dev_appserver.fix_sys_path()
    suite = unittest.loader.TestLoader().discover(test_path, pattern=test_pattern, top_level_dir='.')
    unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    parser = optparse.OptionParser(USAGE)
    options, args = parser.parse_args()
    if len(args) != 3:
        print 'Error: Exactly 3 arguments required.'
        parser.print_help()
        sys.exit(1)
    SDK_PATH = args[0]
    TEST_PATH = args[1]
    PATTERN = args[2]
    main(SDK_PATH, TEST_PATH, PATTERN)