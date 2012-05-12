import unittest2

from google.appengine.ext import testbed
from google.appengine.datastore import datastore_stub_util

from pylib import mock
import dclab
from dclab.promoflight.model.country import Country

class TestCountryModel(unittest2.TestCase):
    """Test case for country model"""

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
        self.get_test_key = Country.add_country('Cebu').name()
        self.update_test_key = Country.add_country('Tacloban').name()
        self.delete_test_key = Country.add_country('Davao').name()

    def tearDown(self):
        self.testbed.deactivate()

    def test_add_country(self):
        c = Country.add_country('Honkong')
        self.assertIsNotNone(c.name())
        # Cleanup
        Country.delete_country(str(c))

    def test_get_none(self):
        c = Country.get_country('xyz')
        self.assertIsNone(c)

    def test_get_existing(self):
        c = Country.get_country(self.get_test_key)
        self.assertEqual(self.get_test_key, c.key().name())
        self.assertEqual('Cebu', c.name)

    def test_update_not_existing(self):
        self.assertIsNone(Country.update_country('xyz123', 'Burf'))

    def test_update_country(self):
        c = Country.get_country(self.update_test_key)
        name = c.name
        k = c.key().name()

        self.assertEquals('Tacloban', name)
        self.assertEquals(k, self.update_test_key)

        del c

        k2 = Country.update_country(self.update_test_key, 'Tacloban 2')
        self.assertIsNotNone(k2)

        a2 = Country.get_country(self.update_test_key)
        self.assertIsNotNone(a2)
        self.assertNotEquals(name, a2.name)
        self.assertEquals('Tacloban 2', a2.name)

    def test_delete_non_existing(self):
        self.assertFalse(Country.delete_country('burf11111'))

    def test_delete_country(self):
        c = Country.delete_country(self.delete_test_key)
        self.assertTrue(c)
        self.assertIsNone(Country.get_country(self.delete_test_key))

    def test_delete_country_with_dependent_fail(self):
        dep = mock.Mock()
        dep.has_countries = mock.Mock()
        dep.has_countries.return_value = True

        c = Country.delete_country(self.delete_test_key, dep)
        self.assertFalse(c)

    def test_delete_country_with_dependent_success(self):
        dep = mock.Mock()
        dep.has_countries = mock.Mock()
        dep.has_countries.return_value = False

        c = Country.delete_country(self.delete_test_key, dep)
        self.assertTrue(c)

    def test_get_countries(self):
        countries = Country.get_countries()
        # Expecting 3 entities
        self.assertEquals(3, countries.count())
        for c in countries:
            self.assertIsInstance(c, Country)