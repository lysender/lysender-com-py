import unittest2

from dclab.promoflight.handler.api import ApiHandler

class TestApiHandler(unittest2.TestCase):
    def test_api_key(self):
        handler = ApiHandler()
        self.assertTrue(len(handler.api_key) > 0)

        handler.api_key = '123'
        self.assertEqual('123', handler.api_key)

if __name__ == '__main__':
    unittest2.main()