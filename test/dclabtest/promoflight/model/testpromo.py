import unittest2
import datetime

from google.appengine.ext import db
from google.appengine.ext import testbed
from google.appengine.datastore import datastore_stub_util

from pylib import mock
import dclab
from dclab.promoflight.model.airline import Airline
from dclab.promoflight.model.location import Location
from dclab.promoflight.model.promo import Promo

class TestPromoModel(unittest2.TestCase):
    """Test case for promo model"""

    template_data = {
        'title': 'Cheapest fare ever',
        'airline': '',
        'origin': '',
        'destination': '',
        'selling_period_start': datetime.date(2012, 2, 20),
        'selling_period_end': datetime.date(2012, 2, 22),
        'travel_period_start': datetime.date(2012, 11, 10),
        'travel_period_end': datetime.date(2012, 12, 15),
        'description': 'This is a sample promo',
    }

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.setup_env(app_id='promoflight')
        self.testbed.activate()
        self.policy = datastore_stub_util.PseudoRandomHRConsistencyPolicy(probability=1)
        self.testbed.init_datastore_v3_stub(consistency_policy=self.policy)

    def tearDown(self):
        self.testbed.deactivate()

    @unittest2.expectedFailure
    def test_add_promo_incomplete_params1(self):
        data = self.template_data.copy()
        del data['airline']
        del data['origin']
        p = Promo.add_promo(data)

    @unittest2.expectedFailure
    def test_add_promo_incomplete_params2(self):
        data = {}
        p = Promo.add_promo(data)

    def test_add_promo_invalid_airline(self):
        origin_key = Location.add_location('Manila')
        destination_key = Location.add_location('Tacloban')

        data = self.template_data.copy()
        data['airline'] = 'zzzz'
        data['origin'] = origin_key
        data['destination'] = destination_key

        p = Promo.add_promo(data)
        self.assertIsNone(p)

    def test_add_promo_invalid_origin(self):
        airline_key = Airline.add_airline('PAL')
        destination_key = Location.add_location('Tacloban')

        data = self.template_data.copy()
        data['airline'] = airline_key
        data['origin'] = 'zzz'
        data['destination'] = destination_key

        p = Promo.add_promo(data)
        self.assertIsNone(p)

    def test_add_promo_invalid_destination(self):
        airline_key = Airline.add_airline('PAL')
        origin_key = Location.add_location('Tacloban')

        data = self.template_data.copy()
        data['airline'] = airline_key
        data['origin'] = origin_key
        data['destination'] = 'zzz'

        p = Promo.add_promo(data)
        self.assertIsNone(p)

    def test_add_promo_success(self):
        airline_key = Airline.add_airline('PAL')
        origin_key = Location.add_location('Manila')
        destination_key = Location.add_location('Tacloban')

        data = self.template_data.copy()
        data['airline'] = airline_key
        data['origin'] = origin_key
        data['destination'] = destination_key

        p = Promo.add_promo(data)
        self.assertIsNotNone(p)

    def test_get_promo_non_existing(self):
        p = Promo.get_promo('123')
        self.assertIsNone(p)

    def test_get_promo_existing(self):
        airline_key = Airline.add_airline('PAL')
        origin_key = Location.add_location('Manila')
        destination_key = Location.add_location('Tacloban')

        data = self.template_data.copy()
        data['airline'] = airline_key
        data['origin'] = origin_key
        data['destination'] = destination_key

        p = Promo.add_promo(data)
        k = p.name()

        pr = Promo.get_promo(k)
        self.assertEquals(k, pr.key().name())
        self.assertEquals(
            Airline.get_airline(airline_key.name()).name,
            pr.airline.name
        )
        self.assertEquals(
            Location.get_location(origin_key.name()).name,
            pr.origin.name
        )
        self.assertEquals(
            Location.get_location(destination_key.name()).name,
            pr.destination.name
        )

    def get_test_update_promo_key(self):
        airline_key = Airline.add_airline('ZestAir')
        origin_key = Location.add_location('Batanes')
        destination_key = Location.add_location('Sulu')

        data = self.template_data.copy()
        data['airline'] = airline_key
        data['origin'] = origin_key
        data['destination'] = destination_key

        p = Promo.add_promo(data)
        return p.name()

    def test_update_promo_invalid_airline(self):
        promo_key = self.get_test_update_promo_key()
        origin_key = Location.add_location('Manila')
        destination_key = Location.add_location('Tacloban')

        data = self.template_data.copy()
        data['airline'] = 'zzzz'
        data['origin'] = origin_key
        data['destination'] = destination_key

        p = Promo.update_promo(promo_key, data)
        self.assertIsNone(p)

    def test_update_promo_invalid_origin(self):
        promo_key = self.get_test_update_promo_key()
        airline_key = Airline.add_airline('PAL')
        destination_key = Location.add_location('Tacloban')

        data = self.template_data.copy()
        data['airline'] = airline_key
        data['origin'] = 'zzz'
        data['destination'] = destination_key

        p = Promo.update_promo(promo_key, data)
        self.assertIsNone(p)

    def test_update_promo_invalid_destination(self):
        promo_key = self.get_test_update_promo_key()
        airline_key = Airline.add_airline('PAL')
        origin_key = Location.add_location('Tacloban')

        data = self.template_data.copy()
        data['airline'] = airline_key
        data['origin'] = origin_key
        data['destination'] = 'zzz'

        p = Promo.update_promo(promo_key, data)
        self.assertIsNone(p)

    def test_update_promo_success(self):
        promo_key = self.get_test_update_promo_key()
        orig_promo_data = Promo.get_promo(promo_key)
        orig_airline = orig_promo_data.airline
        orig_origin = orig_promo_data.origin
        orig_destination = orig_promo_data.destination

        airline_key = Airline.add_airline('PAL')
        origin_key = Location.add_location('Manila')
        destination_key = Location.add_location('Tacloban')

        data = self.template_data.copy()
        data['airline'] = airline_key
        data['origin'] = origin_key
        data['destination'] = destination_key

        p = Promo.update_promo(promo_key, data)
        self.assertIsNotNone(p)

        # Updated promo should have the updated data
        updated_promo = Promo.get_promo(promo_key)
        self.assertNotEqual(orig_airline, updated_promo.airline)
        self.assertNotEqual(orig_origin, updated_promo.origin)
        self.assertNotEqual(orig_destination, updated_promo.destination)

        self.assertEquals(airline_key, updated_promo.airline.key())
        self.assertEquals(origin_key, updated_promo.origin.key())
        self.assertEquals(destination_key, updated_promo.destination.key())

    def test_delete_non_existing(self):
        self.assertFalse(Promo.delete_promo('xyz'))

    def test_delete_success(self):
        promo_key = promo_key = self.get_test_update_promo_key()
        self.assertTrue(Promo.delete_promo(promo_key))
        self.assertIsNone(Promo.get_promo(promo_key))

    def insert_sample_promos(self, limit, **kwargs):
        title_prefix = 'Title'
        airline_value = 'PAL'
        origin_value = 'Tacloban'
        destination_value = 'Manila'

        # Override
        if 'title_prefix' in kwargs:
            title_prefix = kwargs['title_prefix']
        if 'airline_value' in kwargs:
            airline_value = kwargs['airline_value']
        if 'origin_value' in kwargs:
            origin_value = kwargs['origin_value']
        if 'destination_value' in kwargs:
            destination_value = kwargs['destination_value']

        template_data = self.template_data.copy()
        test_data = []

        for i in range(limit):
            test_data.append({'overrides': {'title': '%s %d' % (title_prefix, i)}})

        airline_key = Airline.add_airline(airline_value)
        origin_key = Location.add_location(origin_value)
        destination_key = Location.add_location(destination_value)

        for row in test_data:
            insert_data = template_data.copy()
            insert_data['airline'] = airline_key
            insert_data['origin'] = origin_key
            insert_data['destination'] = destination_key

            for k,v in row['overrides'].iteritems():
                insert_data[k] = v

            Promo.add_promo(insert_data)

    def test_get_latest_promos_empty(self):
        result = Promo.get_latest_promos()
        self.assertIsNone(result)

    def test_get_latest_promos_less_than_10(self):
        self.insert_sample_promos(6)
        result = Promo.get_latest_promos()
        self.assertEqual(6, len(result))

    def test_get_latest_promos_more_than_10(self):
        self.insert_sample_promos(16)
        result = Promo.get_latest_promos()
        self.assertEqual(10, len(result))
        self.assertEquals('Title 15', result[0].title)

    def test_get_latest_promos_more_than_20(self):
        self.insert_sample_promos(29)
        result = Promo.get_latest_promos()
        self.assertEqual(10, len(result))
        self.assertEquals('Title 28', result[0].title)

    def test_get_promo_list_query_query_key(self):
        input_values = [
            {
                'limit': 10,
                'params': {},
                'expected': 'limit=10'
            },
            {
                'limit': 5,
                'params': {},
                'expected': 'limit=5'
            },
            {
                'limit': 10,
                'params': {'keys_only': True},
                'expected': 'limit=10,keys_only=True'
            },
            {
                'limit': 10,
                'params': {'add_date_sort': 'DESC'},
                'expected': 'limit=10,add_date_sort=DESC'
            },
            {
                'limit': 10,
                'params': {'add_date_sort': 'ASC'},
                'expected': 'limit=10,add_date_sort=ASC'
            },
            {
                'limit': 10,
                'params': {'airline': 'foo'},
                'expected': 'limit=10,airline=foo'
            },
            {
                'limit': 10,
                'params': {'origin': 'foo'},
                'expected': 'limit=10,origin=foo'
            },
            {
                'limit': 10,
                'params': {'destination': 'foo'},
                'expected': 'limit=10,destination=foo'
            },
            {
                'limit': 10,
                'params': {'airline': '111', 'origin': '222'},
                'expected': 'limit=10,airline=111,origin=222'
            },
            {
                'limit': 10,
                'params': {'airline': '111', 'origin': '222', 'destination': '333'},
                'expected': 'limit=10,airline=111,origin=222,destination=333'
            },
            {
                'limit': 10,
                'params': {'airline': '111', 'origin': '222', 'destination': '333', 'add_date_sort': 'DESC'},
                'expected': 'limit=10,airline=111,origin=222,destination=333,add_date_sort=DESC'
            },
            {
                'limit': 10,
                'params': {'selling_period_start_sort': 'DESC'},
                'expected': 'limit=10,selling_period_start_sort=DESC'
            },
            {
                'limit': 10,
                'params': {'selling_period_start_sort': 'ASC'},
                'expected': 'limit=10,selling_period_start_sort=ASC'
            },
            {
                'limit': 10,
                'params': {'travel_period_start_sort': 'DESC'},
                'expected': 'limit=10,travel_period_start_sort=DESC'
            },
            {
                'limit': 10,
                'params': {'travel_period_start_sort': 'ASC'},
                'expected': 'limit=10,travel_period_start_sort=ASC'
            },
            {
                'limit': 20,
                'params': {'airline': 'PAL', 'origin': 'mnl', 'destination': 'tac', 'add_date_sort': 'DESC', 'travel_period_start_sort': 'DESC', 'selling_period_start_sort': 'DESC'},
                'expected': 'limit=20,airline=PAL,origin=mnl,destination=tac,add_date_sort=DESC,selling_period_start_sort=DESC,travel_period_start_sort=DESC'
            },
        ]

        for test_input in input_values:
            result = Promo.get_promo_list_query(test_input['limit'], test_input['params'])
            self.assertEquals(test_input['expected'], result['query_key'])

    def test_get_promo_list_query_filters_orders(self):
        input_values = [
            {
                'query': mock.Mock(),
                'params': {'airline': 'air'},
                'filters': [(('airline = ', 'air'), {})],
                'orders': []
            },
            {
                'query': mock.Mock(),
                'params': {'origin': 'orig'},
                'filters': [(('origin = ', 'orig'), {})],
                'orders': []
            },
            {
                'query': mock.Mock(),
                'params': {'destination': 'dest'},
                'filters': [(('destination = ', 'dest'), {})],
                'orders': []
            },
            {
                'query': mock.Mock(),
                'params': {'airline': 'air', 'origin': 'orig'},
                'filters': [(('airline = ', 'air'), {}), (('origin = ', 'orig'), {})],
                'orders': []
            },
            {
                'query': mock.Mock(),
                'params': {'airline': 'air', 'destination': 'dest'},
                'filters': [(('airline = ', 'air'), {}), (('destination = ', 'dest'), {})],
                'orders': []
            },
            {
                'query': mock.Mock(),
                'params': {'airline': 'air', 'origin': 'orig', 'destination': 'dest'},
                'filters': [(('airline = ', 'air'), {}), (('origin = ', 'orig'), {}), (('destination = ', 'dest'), {})],
                'orders': []
            },
            {
                'query': mock.Mock(),
                'params': {'add_date_sort': 'DESC'},
                'filters': [],
                'orders': [(('-add_date',), {})]
            },
            {
                'query': mock.Mock(),
                'params': {'add_date_sort': 'ASC'},
                'filters': [],
                'orders': [(('add_date',), {})]
            },
            {
                'query': mock.Mock(),
                'params': {'airline': 'air', 'add_date_sort': 'DESC'},
                'filters': [(('airline = ', 'air'), {})],
                'orders': [(('-add_date',), {})]
            },
            {
                'query': mock.Mock(),
                'params': {'airline': 'air', 'add_date_sort': 'DESC', 'selling_period_start_sort': 'DESC'},
                'filters': [(('airline = ', 'air'), {})],
                'orders': [(('-add_date',), {}), (('-selling_period_start',), {})]
            },
            {
                'query': mock.Mock(),
                'params': {'travel_period_start_sort': 'DESC'},
                'filters': [],
                'orders': [(('-travel_period_start',), {})]
            },
            {
                'query': mock.Mock(),
                'params': {'add_date_sort': 'DESC', 'selling_period_start_sort': 'DESC', 'travel_period_start_sort': 'DESC'},
                'filters': [],
                'orders': [(('-add_date',), {}), (('-selling_period_start',), {}), (('-travel_period_start',), {})]
            },
            {
                'query': mock.Mock(),
                'params': {'airline': 'air', 'origin': 'orig', 'destination': 'dest', 'add_date_sort': 'DESC', 'selling_period_start_sort': 'DESC', 'travel_period_start_sort': 'DESC'},
                'filters': [(('airline = ', 'air'), {}), (('origin = ', 'orig'), {}), (('destination = ', 'dest'), {})],
                'orders': [(('-add_date',), {}), (('-selling_period_start',), {}), (('-travel_period_start',), {})]
            },
        ]

        for test_input in input_values:
            params = test_input['params']
            params['query'] = test_input['query']
            result = Promo.get_promo_list_query(10, params)

            self.assertEquals(test_input['filters'], test_input['query'].filter.call_args_list)
            self.assertEquals(test_input['orders'], test_input['query'].order.call_args_list)

            self.assertIsInstance(result, dict)
            self.assertIsInstance(result['query'], mock.Mock)
            self.assertIsInstance(result['query_key'], str)

    def test_get_promo_list_airline_filter(self):
        self.insert_sample_promos(5, airline_value='PAL')

        # Test no related airline promo
        result = Promo.get_promo_list(10, {'airline':'XXX'})
        self.assertEquals(0, len(result))

        # Test 5 related airline promos found
        airline_key = Airline.get_airlines()[0].key()

        result = Promo.get_promo_list(10, {'airline': airline_key})
        self.assertEquals(5, len(result))

        for p in result:
            self.assertEquals('PAL', p.airline.name)

    def test_get_promo_list_origin_filter(self):
        self.insert_sample_promos(5, origin_value='Manila', destination_value='Tacloban')

        # Test no related origin promo
        result = Promo.get_promo_list(10, {'origin':'XXX'})
        self.assertEquals(0, len(result))

        # Test 5 related origin promos found
        origins = Location.get_locations()
        origin_key = None
        for o in origins:
            if o.name == 'Manila':
                origin_key = o.key()

        result = Promo.get_promo_list(10, {'origin': origin_key})
        self.assertEquals(5, len(result))

        for p in result:
            self.assertEquals('Manila', p.origin.name)

    def test_get_promo_list_destination_filter(self):
        self.insert_sample_promos(5, origin_value='Manila', destination_value='Tacloban')

        # Test no related destination promo
        result = Promo.get_promo_list(10, {'destination':'XXX'})
        self.assertEquals(0, len(result))

        # Test 5 related destination promos found
        destinations = Location.get_locations()
        destination_key = None
        for d in destinations:
            if d.name == 'Tacloban':
                destination_key = d.key()

        result = Promo.get_promo_list(10, {'destination': destination_key})
        self.assertEquals(5, len(result))

        for p in result:
            self.assertEquals('Tacloban', p.destination.name)

    def test_get_promo_list_mixed_entity_filters(self):
        self.insert_sample_promos(20, airline='PAL', origin_value='Manila', destination_value='Tacloban')

        airline_key = Airline.get_airlines()[0].key()
        locations = Location.get_locations()
        origin_key = None
        destination_key = None
        for loc in locations:
            if loc.name == 'Tacloban':
                destination_key = loc.key()
            elif loc.name == 'Manila':
                origin_key = loc.key()

        result = Promo.get_promo_list(10, {'airline': airline_key, 'origin': origin_key,  'destination': destination_key, 'add_date_sort': 'DESC'})
        self.assertEquals(10, len(result))

        for p in result:
            self.assertEquals('PAL', p.airline.name)
            self.assertEquals('Manila', p.origin.name)
            self.assertEquals('Tacloban', p.destination.name)

    def test_get_promo_list_with_cursor(self):
        self.insert_sample_promos(15)
        cursors = Promo.get_promo_cursors(3, 5, {'add_date_sort': 'DESC'})
        self.assertEquals(5, len(cursors))
        promos = []

        promos.append(Promo.get_promo_list(3, {'add_date_sort': 'DESC'}))
        self.assertEquals(3, len(promos[0]))

        for i,first_batch in enumerate(promos[0]):
            offset = 15 - (i + 1)
            self.assertEquals('Title %s' % offset, first_batch.title)

        for c in cursors:
            ps = Promo.get_promo_list(3, {'start_cursor': c, 'add_date_sort': 'DESC'})
            if ps:
                self.assertEquals(3, len(ps))
                promos.append(ps)

        self.assertEquals(5, len(promos))

        for x,batch in enumerate(promos):
            upper_offset = 15 - (x * 3)
            for y,p in enumerate(batch):
                offset = upper_offset - (y + 1)
                self.assertEquals('Title %d' % offset, p.title)

    def test_get_promo_cursors(self):
        self.insert_sample_promos(15)
        result = Promo.get_promo_cursors(3, 5, {'add_date_sort': 'DESC'})

        self.assertEquals(5, len(result))
        
        for r in result:
            self.assertIsInstance(r, str)

