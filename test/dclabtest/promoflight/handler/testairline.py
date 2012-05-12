import unittest2

from pylib import mock
from dclab.promoflight.handler.airline import AirlineHandler
from dclab.promoflight.model.airline import Airline

from google.appengine.ext import testbed
from google.appengine.datastore import datastore_stub_util

class TestAirlineHandler(unittest2.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.setup_env(app_id='promoflight')
        self.testbed.activate()
        self.policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(probability=1)
        self.testbed.init_datastore_v3_stub(consistency_policy=self.policy)

    def tearDown(self):
        self.testbed.deactivate()

    def test_get_airline_not_found(self):
        handler = AirlineHandler()
        handler.request_params = {'airline_id': '123'}
        result = handler.get_airline()

        self.assertEquals(404, result['code'])

    def test_get_airline(self):
        k = Airline.add_airline('Zebu Pac').name()

        handler = AirlineHandler()
        handler.request_params = {'airline_id': k}
        result = handler.get_airline()

        self.assertEquals('Zebu Pac', result['data']['name'])
        self.assertEquals(k, result['data']['id'])

    def test_get_airlines_empty(self):
        handler = AirlineHandler()
        result = handler.get_airlines()

        self.assertEqual(0, len(result['data']))

    def test_get_airlines_not_empty(self):
        keys = []
        keys.append(Airline.add_airline('Zebu Pac').name())
        keys.append(Airline.add_airline('Cathay Pacific').name())

        handler = AirlineHandler()
        result = handler.get_airlines()
        
        self.assertEquals(2, len(result['data']))
        for row in result['data']:
            self.assertTrue(row['id'] in keys)

    def test_add_airline_invalid_param(self):
        handler = AirlineHandler()
        result = handler.add_airline()

        self.assertEquals(403, result['code'])

    def test_add_airline(self):
        name = 'Boing boing'
        handler = AirlineHandler()
        handler.request_params = {'name': name}
        result = handler.add_airline()

        self.assertFalse('code' in result)
        self.assertTrue(len(result['data']) > 0)

        handler.request_params = {'airline_id': result['data']}
        get_result = handler.get_airline()

        self.assertEquals(name, get_result['data']['name'])

    def test_update_airline_no_id(self):
        handler = AirlineHandler()
        handler.request_params = {'name': 'Boing'}
        result = handler.update_airline()

        self.assertEquals(403, result['code'])

    def test_update_airline_no_name(self):
        handler = AirlineHandler()
        handler.request_params = {'id': '123'}
        result = handler.update_airline()

        self.assertEquals(403, result['code'])

    def test_update_airline_no_id_name(self):
        handler = AirlineHandler()
        result = handler.update_airline()

        self.assertEquals(403, result['code'])

    def test_update_airline_not_found(self):
        airline_id = 'xyz'
        name = 'Boing boing 2'
        handler = AirlineHandler()
        handler.request_params = {'airline_id': airline_id, 'name': name}
        result = handler.update_airline()

        self.assertEquals(500, result['code'])

    def test_update_airline_success(self):
        name = 'Boing boing'
        handler = AirlineHandler()
        handler.request_params = {'name': name}
        result = handler.add_airline()
        k = result['data']

        new_name = 'Boing Voing 2'
        handler.request_params = {'airline_id': k, 'name': new_name}
        update_result = handler.update_airline()

        self.assertEquals(k, update_result['data'])
        
    def test_delete_airline_not_found(self):
        k = '123'
        handler = AirlineHandler()
        handler.request_params = {'airline_id': k}
        result = handler.delete_airline()

        self.assertEquals(500, result['code'])

    def test_delete_airline_success(self):
        name = 'Boing boing'
        handler = AirlineHandler()
        handler.request_params = {'name': name}
        result = handler.add_airline()
        k = result['data']

        handler.request_params = {'airline_id': k}
        result2 = handler.delete_airline()

        self.assertEquals(0, len(result2))

if __name__ == '__main__':
    unittest2.main()