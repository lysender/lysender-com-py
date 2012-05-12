import unittest2
import datetime

from pylib import mock
from pylib import decorator
import dclab

class TestDclab(unittest2.TestCase):
    """Test case for dclab helper functions"""

    date_fail = lambda: [
        [''],
        [None],
        ['xyz'],
        ['2012-00-00'],
        ['2012-0000'],
        ['2012-24-12'],
        ['2012-13-01'],
        ['2012-01-32'],
        ['2012-001-12'],
        ['2012-02-30'],
        ['2011-02-29'],
    ]

    date_fail_format = lambda: [
        ['2012-02-29', '%m/%d/%Y'],
        ['2012-12-25', '%m/%d/%Y'],
    ]

    date_pass = lambda: [
        ['2011-12-25', datetime.datetime(2011, 12, 25)],
        ['2011-02-28', datetime.datetime(2011, 2, 28)],
        ['2012-02-29', datetime.datetime(2012, 2, 29)],
        ['2011-2-2', datetime.datetime(2011, 2, 2)],
    ]

    date_pass_format = lambda: [
        ['2011-12-25', '%Y-%m-%d', datetime.datetime(2011, 12, 25)],
        ['12/25/2011', '%m/%d/%Y', datetime.datetime(2011, 12, 25)],
    ]

    def test_generate_uuid(self):
        self.assertEquals(32, len(dclab.generate_uuid()))

    @decorator.data_provider(date_fail)
    def test_get_valid_date_invalid_no_format(self, input):
        self.assertIsNone(dclab.get_valid_date(input))        

    @decorator.data_provider(date_fail_format)
    def test_get_valid_date_invalid_with_format(self, input, format):
        self.assertIsNone(dclab.get_valid_date(input, format))

    @decorator.data_provider(date_pass)
    def test_get_valid_date_valid_no_format(self, input, expected):
        self.assertEqual(expected, dclab.get_valid_date(input))

    @decorator.data_provider(date_pass_format)
    def test_get_valid_date_valid_with_format(self, input, format, expected):
        self.assertEqual(expected, dclab.get_valid_date(input, format))
