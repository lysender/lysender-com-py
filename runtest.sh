#!/bin/sh
#
# Allow override the test directory and python test script
#
TEST_SCRIPT=${TEST_SCRIPT:-test.py}
TEST_DIR=${TEST_DIR:-test}
PATTERN=${PATTERN:-'test*.py'}

/opt/python/bin/python $TEST_SCRIPT /opt/google-appengine/ $TEST_DIR "$PATTERN"
