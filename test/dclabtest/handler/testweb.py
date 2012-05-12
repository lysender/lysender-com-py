import unittest2
import hmac
import hashlib
import simplejson as json

from pylib import mock
from pylib import decorator
from dclab.handler import web

class TestWebHandler(unittest2.TestCase):
    
    controller_path_provider = lambda: [
        ['/', [], 'index']
    ]

    @decorator.data_provider(controller_path_provider)
    def test_controller_path(self, path, admin_dirs, expected):
        w = web.WebHandler()
        self.assertEquals(expected, w.get_controller_path(path, admin_dirs))