import unittest2

from google.appengine.ext import testbed
from google.appengine.datastore import datastore_stub_util

from pylib import mock
import dclab
from dclab.promoflight.model.location import Location

class TestLocationModel(unittest2.TestCase):
    """Test case for location model"""

    get_test_key = None
    update_test_key = None
    delete_test_key = None

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.setup_env(app_id='promoflight')
        self.testbed.activate()
        self.policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(probability=1)
        self.testbed.init_datastore_v3_stub(consistency_policy=self.policy)

        # Test data for get and update
        self.get_test_key = Location.add_location('Cebu').name()
        self.update_test_key = Location.add_location('Tacloban').name()
        self.delete_test_key = Location.add_location('Davao').name()

    def tearDown(self):
        self.testbed.deactivate()

    def test_add_location(self):
        l = Location.add_location('Subic')
        self.assertIsNotNone(l.name())
        # Cleanup
        Location.delete_location(str(l))

    def test_get_none(self):
        l = Location.get_location('xyz')
        self.assertIsNone(l)

    def test_get_existing(self):
        l = Location.get_location(self.get_test_key)
        self.assertEqual(self.get_test_key, l.key().name())
        self.assertEqual('Cebu', l.name)

    def test_update_not_existing(self):
        self.assertIsNone(Location.update_location('xyz123', 'Burf'))

    def test_update_location(self):
        l = Location.get_location(self.update_test_key)
        name = l.name
        k = l.key().name()

        self.assertEquals('Tacloban', name)
        self.assertEquals(k, self.update_test_key)

        del l

        k2 = Location.update_location(self.update_test_key, 'Tacloban 2')
        self.assertIsNotNone(k2)

        a2 = Location.get_location(self.update_test_key)
        self.assertIsNotNone(a2)
        self.assertNotEquals(name, a2.name)
        self.assertEquals('Tacloban 2', a2.name)

    def test_delete_non_existing(self):
        self.assertFalse(Location.delete_location('burf11111'))

    def test_delete_location(self):
        l = Location.delete_location(self.delete_test_key)
        self.assertTrue(l)
        self.assertIsNone(Location.get_location(self.delete_test_key))

    def test_delete_location_with_dependent_fail(self):
        dep = mock.Mock()
        dep.has_locations = mock.Mock()
        dep.has_locations.return_value = True

        l = Location.delete_location(self.delete_test_key, dep)
        self.assertFalse(l)

    def test_delete_location_with_dependent_success(self):
        dep = mock.Mock()
        dep.has_locations = mock.Mock()
        dep.has_locations.return_value = False

        l = Location.delete_location(self.delete_test_key, dep)
        self.assertTrue(l)

    def test_get_locations(self):
        locs = Location.get_locations()
        # Expecting 3 entities
        self.assertEquals(3, locs.count())
        for loc in locs:
            self.assertIsInstance(loc, Location)