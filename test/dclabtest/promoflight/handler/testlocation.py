import unittest2

from pylib import mock
from dclab.promoflight.handler.location import LocationHandler
from dclab.promoflight.model.location import Location

from google.appengine.ext import testbed
from google.appengine.datastore import datastore_stub_util

class TestLocationHandler(unittest2.TestCase):

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.setup_env(app_id='promoflight')
        self.testbed.activate()
        self.policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(probability=1)
        self.testbed.init_datastore_v3_stub(consistency_policy=self.policy)

    def tearDown(self):
        self.testbed.deactivate()

    def test_get_location_not_found(self):
        handler = LocationHandler()
        handler.request_params = {'location_id': '123'}
        result = handler.get_location()
        self.assertEquals(404, result['code'])

    def test_get_location(self):
        k = Location.add_location('Cebu').name()

        handler = LocationHandler()
        handler.request_params = {'location_id': k}
        result = handler.get_location()

        self.assertEquals('Cebu', result['data']['name'])
        self.assertEquals(k, result['data']['id'])

    def test_get_locations_empty(self):
        handler = LocationHandler()
        result = handler.get_locations()

        self.assertEqual(0, len(result['data']))

    def test_get_locations_not_empty(self):
        keys = []
        keys.append(Location.add_location('Cebu').name())
        keys.append(Location.add_location('Tacloban').name())

        handler = LocationHandler()
        result = handler.get_locations()
        
        self.assertEquals(2, len(result['data']))
        for row in result['data']:
            self.assertTrue(row['id'] in keys)

    def test_add_location_invalid_param(self):
        handler = LocationHandler()
        result = handler.add_location()

        self.assertEquals(403, result['code'])

    def test_add_location_empty_name(self):
        handler = LocationHandler()
        handler.request_params = {'name': ''}
        result = handler.add_location()

        self.assertEquals(403, result['code'])

    def test_add_location(self):
        name = 'Mactan'
        handler = LocationHandler()
        handler.request_params = {'name': name}
        result = handler.add_location()

        self.assertFalse('code' in result)
        self.assertTrue(len(result['data']) > 0)

        handler.request_params = {'location_id': result['data']}
        get_result = handler.get_location()

        self.assertEquals(name, get_result['data']['name'])

    def test_update_location_no_id(self):
        handler = LocationHandler()
        handler.request_params = {'name': 'Cebu'}
        result = handler.update_location()

        self.assertEquals(403, result['code'])

    def test_update_location_no_name(self):
        handler = LocationHandler()
        handler.request_params = {'id': '123'}
        result = handler.update_location()

        self.assertEquals(403, result['code'])

    def test_update_location_no_id_name(self):
        handler = LocationHandler()
        result = handler.update_location()

        self.assertEquals(403, result['code'])

    def test_update_location_not_found(self):
        location_id = 'xyz'
        name = 'Subic'
        handler = LocationHandler()
        handler.request_params = {'location_id': location_id, 'name': name}
        result = handler.update_location()

        self.assertEquals(500, result['code'])

    def test_update_location_success(self):
        name = 'Subic'
        handler = LocationHandler()
        handler.request_params = {'name': name}
        result = handler.add_location()
        k = result['data']

        new_name = 'Subic Bay'
        handler.request_params = {'location_id': k, 'name': new_name}
        update_result = handler.update_location()

        self.assertEquals(k, update_result['data'])
        
    def test_delete_location_not_found(self):
        k = '123'
        handler = LocationHandler()
        handler.request_params = {'location_id': k}
        result = handler.delete_location()

        self.assertEquals(500, result['code'])

    def test_delete_location_success(self):
        name = 'Boing boing'
        handler = LocationHandler()
        handler.request_params = {'name': name}
        result = handler.add_location()
        k = result['data']

        handler.request_params = {'location_id': k}
        result2 = handler.delete_location()

        self.assertEquals(0, len(result2))


if __name__ == '__main__':
    unittest2.main()