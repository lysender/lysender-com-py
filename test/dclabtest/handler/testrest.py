import unittest2
import hmac
import hashlib
import simplejson as json

from pylib import mock
from pylib import decorator
from dclab.handler import rest

class TestRestHandler(unittest2.TestCase):
    def test_rest_object(self):
        r = rest.RestHandler()
        self.assertIsNotNone(r.api_methods)

    method_provider = lambda: [
        ['get'], 
        ['post'], 
        ['put'], 
        ['delete'], 
        ['head'], 
        ['trace'],
    ]

    is_action_valid_provider = lambda: [
        # api_methods, input, expected
        [
            {},
            {
                'get': ['foo', 'bar'],
                'post': ['fooo'],
                'test': ['joe', 'brad']
            },
            False
        ],
        [
            {
                'get': [],
                'post': []
            },
            {
                'get': ['foo', 'bar'],
                'post': ['fooo'],
                'test': ['joe', 'brad']
            },
            False
        ],
        [
            {
                'get': ['xxx', 'yyy', 'zzz'],
                'post': []
            },
            {
                'get': ['foo', 'bar'],
                'post': ['fooo'],
                'test': ['joe', 'brad']
            },
            False
        ],
        [
            {
                'get': ['foo', 'bar'],
                'post': ['fooo'],
                'test': ['joe', 'brad']
            },
            {
                'get': ['foo', 'bar'],
                'post': ['fooo'],
                'test': ['joe', 'brad']
            },
            True
        ],
    ]

    @decorator.data_provider(method_provider)
    def test_methods(self, method):
        """Assert that all methods are existing on bare rest handler"""
        r = rest.RestHandler()
        self.assertIsNotNone(getattr(r, method, None))

    @decorator.data_provider(is_action_valid_provider)
    def test_is_action_valid(self, api_methods, input, expected):
        """Assert that an action is valid for the given handler configuration"""
        r = rest.RestHandler()
        r.api_methods = api_methods

        if api_methods:
            for api_method, api_actions in api_methods.iteritems():
                setattr(r, api_method, lambda: 1)
                for api_action in api_actions:
                    setattr(r, api_action, lambda: 1)

        for method, actions in input.iteritems():
            for action in actions:
                self.assertEquals(expected, r.is_action_valid(method, action))

    def test_signature(self):
        """Assert that signature on parameters matched"""

        # Sample signature routine
        msg = ''.join(['action', 
                       'get_recent_promos', 
                       'end_date', 
                       '2012-01-01',
                       'key',
                       '123456',
                       'start_date',
                       '2012-02-14'
                       ])
        signature_sample = hmac.new('123456', msg, hashlib.sha256).hexdigest()

        input_values = [
            {
                'parameters': {
                    'action': 'do',
                    'foo': 'bar',
                    'sig': 'xxxxxxxxxxxxxxx',
                    'key': 'burf'
                },
                'key': 'burf',
                'signature': 'burffailed',
                'expected': False
            },
            {
                'parameters': {
                    'action': 'get_recent_promos',
                    'key': '123456',
                    'start_date': '2012-02-14',
                    'end_date': '2012-01-01',
                    'sig': signature_sample
                },
                'key': '123456',
                'signature': signature_sample,
                'expected': True
            }
        ]

        for test_input in input_values:
            gen_sig = rest.generate_signature(test_input['key'], test_input['parameters'])
            self.assertEquals(test_input['expected'], 
                              test_input['signature'] == gen_sig)

    def test_is_key_valid_none(self):
        r = rest.RestHandler()
        self.assertFalse(r.is_key_valid('xyz'))

    def test_is_key_valid_invalid(self):
        r = rest.RestHandler()
        r.api_key = 'xyz'
        self.assertFalse(r.is_key_valid('123'))

    def test_is_key_valid_valid(self):
        r = rest.RestHandler()
        r.api_key = 'xyz'
        self.assertTrue(r.is_key_valid('xyz'))

    def test_get_api_action(self):
        input_values = [
            {
                'parameters': {},
                'expected': None
            },
            {
                'parameters': {'foo': 'bar', 'bar': 'foo', 'po': 'po'},
                'expected': None
            },
            {
                'parameters': {'exion': 'do_stuff'},
                'expected': None
            },
            {
                'parameters': {'action': 'do_stuff'},
                'expected': 'do_stuff'
            },
            {
                'parameters': {'test': 'order', 'action': 'test_order'},
                'expected': 'test_order'
            }
        ]

        r = rest.RestHandler()
        for test_input in input_values:
            self.assertEquals(
                test_input['expected'], 
                r.get_api_action(test_input['parameters'])
            )

    def test_get_api_params(self):
        sample_params = {
            'foo': '1',
            'bar': 'xxx',
            'sig': 'test_sig'
        }

        def get_side_effect(key, default_value=''):
            if key in sample_params:
                return sample_params[key]

            return default_value

        r = rest.RestHandler()
        r.request = mock.Mock()
        r.request.arguments.return_value = ['foo', 'bar', 'sig']
        r.request.get.side_effect = get_side_effect

        self.assertEquals(sample_params, r.get_api_params())

    def test_get_api_params_empty(self):
        sample_params = {}

        def get_side_effect(key, default_value=''):
            if key in sample_params:
                return sample_params[key]

            return default_value

        r = rest.RestHandler()
        r.request = mock.Mock()
        r.request.arguments.return_value = []
        r.request.get.side_effect = get_side_effect

        self.assertEquals({}, r.get_api_params())

    def test_get_api_param_empty(self):
        r = rest.RestHandler()
        self.assertIsNone(r.get_api_param('foo'))

    def test_get_api_param_not_exists(self):
        r = rest.RestHandler()
        r.request_params = {'foo': 'bar', 'q': 'mirror'}
        self.assertIsNone(r.get_api_param('keyword'))

    def test_get_api_param_exists(self):
        r = rest.RestHandler()
        r.request_params = {'foo': 'bar', 'q': 'mirror'}
        self.assertEqual('mirror', r.get_api_param('q'))

    def test_init_action(self):
        sample_params = {
            'action': 'get_stuff',
            'api_key': '123',
            'domain_name': 'stuff.com',
            'sig': '1f20b57760381ecca22dc0d695cff4d192905ebe06441a4b8f93b30b2e9d709a'
        }

        r = rest.RestHandler()

        # Setup key
        r.api_key = '123'
        r.get_api_params = mock.Mock()
        r.get_api_params.return_value = sample_params

        # Setup method and action
        r.api_methods['get'].append('get_stuff')
        r.get = mock.Mock()
        r.get_stuff = mock.Mock()

        # Run test
        self.assertTrue(r.init_action('get'))

    def test_do_action(self):
        r = rest.RestHandler()
        r.request = mock.Mock()
        r.response = mock.Mock()

        r.init_action = mock.Mock()
        r.init_action.return_value = True
        r.request_action = 'get_stuff'
        r.get_stuff = mock.Mock()
        r.get_stuff.return_value = 'bar'

        ret = r.do_action('get')
        self.assertEquals('bar', ret)

    def test_generate_response_empty(self):
        r = rest.RestHandler()
        result = r.generate_response({})
        expected = {'code': 200, 'message': 'Success'}

        self.assertEquals(expected, result)

    def test_generate_response_error(self):
        r = rest.RestHandler()
        result = r.generate_response({'code': 404, 'message': 'Record not found'})
        expected = {'code': 404, 'message': 'Record not found'}

        self.assertEquals(expected, result)

    def test_generate_response_error_with_data(self):
        r = rest.RestHandler()
        result = r.generate_response({
            'data': {'foo': 'bar', 'google': 'doodle'},
            'code': 403,
            'message': 'Permission denied'
        })
        expected = {
            'code': 403, 
            'message': 'Permission denied', 
            'data': {'foo': 'bar', 'google': 'doodle'}
        }
        self.assertEquals(expected, result)

    def test_generic_get_post_403(self):
        r = rest.RestHandler()
        r.do_action = mock.Mock()
        r.do_action.return_value = False
        r.response = mock.Mock()
        r.response.headers = {}

        r.get()
        r.post()
        get_call = r.response.out.method_calls[0]
        post_call = r.response.out.method_calls[1]

        self.assertEquals(json.dumps({'code': 403, 'message': 'Invalid parameters'}), get_call[1][0])
        self.assertEquals(json.dumps({'code': 403, 'message': 'Invalid parameters'}), post_call[1][0])

    def test_generic_get_post_success(self):
        r = rest.RestHandler()
        r.do_action = mock.Mock()
        r.do_action.return_value = {'foo': 'bar'}
        r.response = mock.Mock()
        r.response.headers = {}

        r.get()
        r.post()
        get_call = r.response.out.method_calls[0]
        post_call = r.response.out.method_calls[1]

        self.assertEquals(json.dumps({'foo': 'bar', 'code': 200, 'message': 'Success'}), get_call[1][0])
        self.assertEquals(json.dumps({'foo': 'bar', 'code': 200, 'message': 'Success'}), post_call[1][0])

if __name__ == '__main__':
    unittest2.main()
