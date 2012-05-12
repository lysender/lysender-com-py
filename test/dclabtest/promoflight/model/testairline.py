import unittest2

from google.appengine.ext import testbed
from google.appengine.datastore import datastore_stub_util

from pylib import mock
import dclab
from dclab.promoflight.model.airline import Airline

class TestAirlineModel(unittest2.TestCase):
    """Test case for airline model"""

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
        self.get_test_key = Airline.add_airline('PAL').name()
        self.update_test_key = Airline.add_airline('Zest Air').name()
        self.delete_test_key = Airline.add_airline('Silhig Air').name()

    def tearDown(self):
        self.testbed.deactivate()

    def test_add_airline(self):
        a = Airline.add_airline('Cebu Pacific')
        self.assertIsNotNone(a.name())
        # Cleanup
        Airline.delete_airline(str(a))

    def test_get_none(self):
        a = Airline.get_airline('xyz')
        self.assertIsNone(a)

    def test_get_existing(self):
        a = Airline.get_airline(self.get_test_key)
        self.assertEqual(self.get_test_key, a.key().name())
        self.assertEqual('PAL', a.name)

    def test_update_not_existing(self):
        self.assertIsNone(Airline.update_airline('xyz123', 'Burf'))

    def test_update_airline(self):
        a = Airline.get_airline(self.update_test_key)
        name = a.name
        k = a.key().name()

        self.assertEquals('Zest Air', name)
        self.assertEquals(k, self.update_test_key)

        del a

        k2 = Airline.update_airline(self.update_test_key, 'ZestAir')
        self.assertIsNotNone(k2)

        a2 = Airline.get_airline(self.update_test_key)
        self.assertIsNotNone(a2)
        self.assertNotEquals(name, a2.name)
        self.assertEquals('ZestAir', a2.name)

    def test_delete_non_existing(self):
        self.assertFalse(Airline.delete_airline('burf11111'))

    def test_delete_airline(self):
        a = Airline.delete_airline(self.delete_test_key)
        self.assertTrue(a)
        self.assertIsNone(Airline.get_airline(self.delete_test_key))

    def test_delete_airline_with_dependent_fail(self):
        dep = mock.Mock()
        dep.has_airlines = mock.Mock()
        dep.has_airlines.return_value = True

        a = Airline.delete_airline(self.delete_test_key, dep)
        self.assertFalse(a)

    def test_delete_airline_with_dependent_success(self):
        dep = mock.Mock()
        dep.has_airlines = mock.Mock()
        dep.has_airlines.return_value = False

        a = Airline.delete_airline(self.delete_test_key, dep)
        self.assertTrue(a)

    def test_get_airlines(self):
        airs = Airline.get_airlines()
        # Expecting 3 entities
        self.assertEquals(3, airs.count())
        for air in airs:
            self.assertIsInstance(air, Airline)