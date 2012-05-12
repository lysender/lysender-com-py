import unittest2
import datetime

import dclab

from pylib import mock
from dclab.promoflight.handler.promo import PromoHandler
from dclab.promoflight.model.location import Location
from dclab.promoflight.model.airline import Airline
from dclab.promoflight.model.promo import Promo

from google.appengine.ext import testbed
from google.appengine.datastore import datastore_stub_util

class TestPromoHandler(unittest2.TestCase):

    template_data = {
        'title': 'Cheapest fare ever',
        'airline_id': '',
        'origin_id': '',
        'destination_id': '',
        'selling_period_start': '2012-2-20',
        'selling_period_end': '2012-2-22',
        'travel_period_start': '2012-11-10',
        'travel_period_end': '2012-1-15',
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

    def test_get_promo_not_found(self):
        handler = PromoHandler()
        handler.request_params = {'promo_id': 'xyz'}
        result = handler.get_promo_detail()
        self.assertEquals(404, result['code'])

    def get_sample_promo(self):
        airline_key = Airline.add_airline('ZestAir')
        origin_key = Location.add_location('Batanes')
        destination_key = Location.add_location('Sulu')

        data = self.template_data.copy()
        data['airline'] = airline_key
        data['origin'] = origin_key
        data['destination'] = destination_key

        raw_data = data.copy()

        del raw_data['airline']
        del raw_data['origin']
        del raw_data['destination']

        raw_data['airline_id'] = airline_key.name()
        raw_data['origin_id'] = origin_key.name()
        raw_data['destination_id'] = destination_key.name()

        dates = [
            'selling_period_start',
            'selling_period_end',
            'travel_period_start',
            'travel_period_end'
        ]

        for k in dates:
            d = dclab.get_valid_date(data[k])
            data[k] = datetime.date(d.year, d.month, d.day)

        p = Promo.add_promo(data)
        ret = {'id': p.name(), 'raw_data': raw_data}

        return ret

    def get_formatted_promo(self, unique_id):
        p = Promo.get_promo(unique_id)
        data = {}
        data['promo_id'] = p.key().name()
        data['title'] = p.title
        data['airline_id'] = p.airline.key().name()
        data['origin_id'] = p.origin.key().name()
        data['destination_id'] = p.destination.key().name()
        data['selling_period_start'] = p.selling_period_start.strftime('%Y-%m-%d')
        data['selling_period_end'] = p.selling_period_end.strftime('%Y-%m-%d')
        data['travel_period_start'] = p.travel_period_start.strftime('%Y-%m-%d')
        data['travel_period_end'] = p.travel_period_end.strftime('%Y-%m-%d')
        data['description'] = p .description

        return data

    def test_get_promo_detail(self):
        p = self.get_sample_promo()
        k = p['id']

        handler = PromoHandler()
        handler.request_params = {'promo_id': k}
        result = handler.get_promo_detail()

        self.assertEquals(self.template_data['title'], result['data']['title'])
        self.assertEquals(k, result['data']['id'])

    def test_add_promo_invalid_params(self):
        template_data = self.get_sample_promo()['raw_data']
        input_values = [
            # Empty parameters
            {
                'template_param': {},
                'override_params': {},
                'expected_code': 403
            },
            # No airline and origin
            {
                'template_param': template_data.copy(),
                'delete_params': ['airline_id', 'origin_id'],
                'expected_code': 403
            },
            # Invalid airline
            {
                'template_param': template_data.copy(),
                'override_params': {'airline_id': 'xyz'},
                'expected_code': 403
            },
            # Invalid origin
            {
                'template_param': template_data.copy(),
                'override_params': {'origin_id': 'xyz'},
                'expected_code': 403
            },
            # Invalid destination
            {
                'template_param': template_data.copy(),
                'override_params': {'destination_id': 'xyz'},
                'expected_code': 403
            },
            # Invalid travel start date
            {
                'template_param': template_data.copy(),
                'override_params': {'travel_period_start': 'xyz'},
                'expected_code': 403
            },
            # Invalid travel end date
            {
                'template_param': template_data.copy(),
                'override_params': {'travel_period_end': 'xyz'},
                'expected_code': 403
            },
            # Invalid selling start date
            {
                'template_param': template_data.copy(),
                'override_params': {'selling_period_start': 'xyz'},
                'expected_code': 403
            },
            # Invalid selling end date
            {
                'template_param': template_data.copy(),
                'override_params': {'selling_period_end': 'xyz'},
                'expected_code': 403
            },
        ]

        for test_input in input_values:
            handler =  PromoHandler()
            if 'template_param' in test_input:
                handler.request_params = test_input['template_param']
            if 'override_params' in test_input:
                for override_key, override_value in test_input['override_params'].iteritems():
                    handler.request_params[override_key] = override_value
            if 'delete_params' in test_input:
                for del_param in test_input['delete_params']:
                    del handler.request_params[del_param]

            self.assertEquals(test_input['expected_code'], handler.add_promo()['code'])

    def test_add_promo(self):
        handler = PromoHandler()
        template_data = self.get_sample_promo()['raw_data']
        handler.request_params = template_data.copy()
        result = handler.add_promo()
        
        self.assertFalse('code' in result)
        self.assertTrue(len(result['data']) > 0)

        handler.request_params = {'promo_id': result['data']}
        get_result = handler.get_promo_detail()

        self.assertEquals(self.template_data['title'], get_result['data']['title'])

    def test_update_promo_invalid_params(self):
        sample_promo = self.get_sample_promo()
        template_data = sample_promo['raw_data']
        template_data['promo_id'] = sample_promo['id']
        input_values = [
            # Empty parameters
            {
                'template_param': {},
                'override_params': {},
                'expected_code': 403
            },
            # No promo id
            {
                'template_param': template_data,
                'delete_params': ['promo_id'],
                'expected_code': 403
            },
            # Invalid promo id
            {
                'template_param': template_data,
                'override_params': {'promo_id': 'xyz'},
                'expected_code': 500
            },
            # Invalid airline
            {
                'template_param': template_data.copy(),
                'override_params': {'airline_id': 'xyz'},
                'expected_code': 403
            },
            # Invalid origin
            {
                'template_param': template_data.copy(),
                'override_params': {'origin_id': 'xyz'},
                'expected_code': 403
            },
            # Invalid destination
            {
                'template_param': template_data.copy(),
                'override_params': {'destination_id': 'xyz'},
                'expected_code': 403
            },
            # Invalid travel start date
            {
                'template_param': template_data.copy(),
                'override_params': {'travel_period_start': 'xyz'},
                'expected_code': 403
            },
            # Invalid travel end date
            {
                'template_param': template_data.copy(),
                'override_params': {'travel_period_end': 'xyz'},
                'expected_code': 403
            },
            # Invalid selling start date
            {
                'template_param': template_data.copy(),
                'override_params': {'selling_period_start': 'xyz'},
                'expected_code': 403
            },
            # Invalid selling end date
            {
                'template_param': template_data.copy(),
                'override_params': {'selling_period_end': 'xyz'},
                'expected_code': 403
            },
        ]

        for test_input in input_values:
            handler =  PromoHandler()
            if 'template_param' in test_input:
                handler.request_params = test_input['template_param']
            if 'override_params' in test_input:
                for override_key, override_value in test_input['override_params'].iteritems():
                    handler.request_params[override_key] = override_value
            if 'delete_params' in test_input:
                for del_param in test_input['delete_params']:
                    del handler.request_params[del_param]

            result = handler.update_promo()
            self.assertEquals(test_input['expected_code'], result['code'])

    def test_update_promo_success(self):
        sample_promo = self.get_sample_promo()
        template_data = sample_promo['raw_data']
        template_data['promo_id'] = sample_promo['id']
        new_airline_id = Airline.add_airline('Cathay Pacific').name()
        new_origin_id = Location.add_location('Japan').name()
        new_destination_id = Location.add_location('Macau').name()
        input_values = [
            # Complete parameters
            {
                'template_param': template_data
            },
            # Title updated
            {
                'template_param': template_data,
                'override_params': {'title': 'New shining title'},
                'expected_updates': {
                    'title': 'New shining title'
                }
            },
            # Description updated
            {
                'template_param': template_data,
                'override_params': {'description': 'Awesome promo fare right here right now'},
                'expected_updates': {
                    'description': 'Awesome promo fare right here right now'
                }
            },
            # Travel period updated
            {
                'template_param': template_data.copy(),
                'override_params': {'travel_period_start': '2012-09-01', 'travel_period_end': '2012-09-30'},
                'expected_updates': {
                    'travel_period_start': '2012-09-01', 
                    'travel_period_end': '2012-09-30'
                }
            },
            # Selling period updated
            {
                'template_param': template_data.copy(),
                'override_params': {'selling_period_start': '2012-09-01', 'selling_period_end': '2012-09-30'},
                'expected_updates': {
                    'selling_period_start': '2012-09-01', 
                    'selling_period_end': '2012-09-30'
                }
            },
            # Airline updated
            {
                'template_param': template_data.copy(),
                'override_params': {'airline_id': new_airline_id},
                'expected_updates': {
                    'airline_id': new_airline_id
                }
            },
            # Origin updated
            {
                'template_param': template_data.copy(),
                'override_params': {'origin_id': new_origin_id},
                'expected_updates': {
                    'origin_id': new_origin_id
                }
            },
            # Destination updated
            {
                'template_param': template_data.copy(),
                'override_params': {'destination_id': new_destination_id},
                'expected_updates': {
                    'destination_id': new_destination_id
                }
            }
        ]
        for test_input in input_values:
            handler =  PromoHandler()
            if 'template_param' in test_input:
                handler.request_params = test_input['template_param']
            if 'override_params' in test_input:
                for override_key, override_value in test_input['override_params'].iteritems():
                    handler.request_params[override_key] = override_value
            if 'delete_params' in test_input:
                for del_param in test_input['delete_params']:
                    del handler.request_params[del_param]

            result = handler.update_promo()
            self.assertFalse('code' in result)
            self.assertEquals(test_input['template_param']['promo_id'], result['data'])

            if 'expected_updates' in test_input:
                the_promo = self.get_formatted_promo(test_input['template_param']['promo_id'])
                for expected_update_key, expected_update_val in test_input['expected_updates'].iteritems():
                    self.assertEquals(expected_update_val, the_promo[expected_update_key])

    def test_delete_promo_no_param(self):
        k = '123'
        handler = PromoHandler()
        handler.request_params = {}
        result = handler.delete_promo()

        self.assertEquals(403, result['code'])
        
    def test_delete_promo_not_found(self):
        k = '123'
        handler = PromoHandler()
        handler.request_params = {'promo_id': k}
        result = handler.delete_promo()

        self.assertEquals(500, result['code'])

    def test_delete_success(self):
        sample_promo = self.get_sample_promo()
        handler = PromoHandler()
        handler.request_params = {'promo_id': sample_promo['id']}
        result = handler.delete_promo()

        self.assertEquals(0, len(result))
        self.assertIsNone(Promo.get_promo(sample_promo['id']))

    def insert_sample_promos(self, limit, **kwargs):
        title_value = 'Title'
        airline_value = 'PAL'
        origin_value = 'Manila'
        destination_value = 'Tacloban'
        ref_data = {}
        airline_key = None
        origin_key = None
        destination_key = None

        if 'title_value' in kwargs:
            title_value = kwargs['title_value']
        if 'airline_value' in kwargs:
            airline_value = kwargs['airline_value']
        if 'origin_value' in kwargs:
            origin_value = kwargs['origin_value']
        if 'destination_value' in kwargs:
            destination_value = kwargs['destination_value']
        if 'ref_data' in kwargs:
            ref_data = kwargs['ref_data']

        template_data = self.template_data.copy()
        test_data = []

        for i in range(limit):
            test_data.append({'overrides': {'title': '%s %d' % (title_value, i)}})

        if 'airline_key' in kwargs:
            airline_key = kwargs['airline_key']
        else:
            airline_key = Airline.add_airline(airline_value)
            ref_data['airline_key'] = airline_key

        if 'origin_key' in kwargs:
            origin_key = kwargs['origin_key']
        else:            
            origin_key = Location.add_location(origin_value)
            ref_data['origin_key'] = origin_key

        if 'destination_key' in kwargs:
            destination_key = kwargs['destination_key']
        else:
            destination_key = Location.add_location(destination_value)
            ref_data['destination_key'] =destination_key

        date_fields = ['selling_period_start', 'selling_period_end', 'travel_period_start', 'travel_period_end']

        for row in test_data:
            insert_data = template_data.copy()
            insert_data['airline'] = airline_key
            insert_data['origin'] = origin_key
            insert_data['destination'] = destination_key

            for k,v in row['overrides'].iteritems():
                insert_data[k] = v

            for k in date_fields:
                if k in insert_data:
                    tmp_date = dclab.get_valid_date(insert_data[k])
                    insert_data[k] = datetime.date(tmp_date.year, tmp_date.month, tmp_date.day)

            Promo.add_promo(insert_data)

    def test_get_latest_promos_empty(self):
        handler = PromoHandler()
        handler.request_params = {}
        result = handler.get_latest_promos()
        self.assertEqual(0, (result['data']['count']))

    def test_get_latest_promos_less_than_10(self):
        self.insert_sample_promos(7, airline_value='PAL', origin_value='Manila', destination_value='Tacloban')
        handler = PromoHandler()
        handler.request_params = {}
        result = handler.get_latest_promos()
        self.assertEqual(7, (result['data']['count']))
        self.assertEqual('Title 6', result['data']['promos'][0]['title'])

        # Test individual contents
        for row in result['data']['promos']:
            self.assertEquals('PAL', row['airline']['name'])
            self.assertEquals('Manila', row['origin']['name'])
            self.assertEquals('Tacloban', row['destination']['name'])

    def test_get_latest_promos_more_than_10(self):
        self.insert_sample_promos(17, airline_value='PAL', origin_value='Manila', destination_value='Tacloban')
        handler = PromoHandler()
        handler.request_params = {}
        result = handler.get_latest_promos()
        self.assertEqual(10, (result['data']['count']))
        self.assertEqual('Title 16', result['data']['promos'][0]['title'])

        # Test individual contents
        for row in result['data']['promos']:
            self.assertEquals('PAL', row['airline']['name'])
            self.assertEquals('Manila', row['origin']['name'])
            self.assertEquals('Tacloban', row['destination']['name'])

    def test_get_latest_promos_more_than_20(self):
        self.insert_sample_promos(27, airline_value='PAL', origin_value='Manila', destination_value='Tacloban')
        handler = PromoHandler()
        handler.request_params = {}
        result = handler.get_latest_promos()
        self.assertEqual(10, (result['data']['count']))
        self.assertEqual('Title 26', result['data']['promos'][0]['title'])

        # Test individual contents
        for row in result['data']['promos']:
            self.assertEquals('PAL', row['airline']['name'])
            self.assertEquals('Manila', row['origin']['name'])
            self.assertEquals('Tacloban', row['destination']['name'])

    def test_get_promo_list_invalid_params(self):
        input_values = [
            {
                'params': {},
                'expected': {'code': 403}
            },
            {
                'params': {'limit': u''},
                'expected': {'code': 403}
            },
            {
                'params': {'limit': u'xyz'},
                'expected': {'code': 403}
            },
            {
                'params': {'limit': u'100.00'},
                'expected': {'code': 403}
            },
            {
                'params': {'limit': u'0'},
                'expected': {'code': 403}
            },
            {
                'params': {'limit': u'100'},
                'expected': {'code': 403}
            },
            {
                'params': {'limit': u'10', 'airline_id': u'XYZ'},
                'expected': {'code': 403}
            },
            {
                'params': {'limit': u'10', 'add_date_sort': u''},
                'expected': {'code': 403}
            },
            {
                'params': {'limit': u'10', 'add_date_sort': u'xyz'},
                'expected': {'code': 403}
            },
            {
                'params': {'limit': u'10', 'add_date_sort': u'asc'},
                'expected': {'code': 403}
            },
            {
                'params': {'limit': u'10', 'add_date_sort': u'desc'},
                'expected': {'code': 403}
            },
        ]

        for test_input in input_values:
            handler = PromoHandler()
            handler.request_params = test_input['params']
            result = handler.get_promo_list()

            for expected_key,expected_value in test_input['expected'].iteritems():
                self.assertEquals(expected_value, result[expected_key])

    def test_get_promo_list_less_than_limit(self):
        self.insert_sample_promos(7, airline_value='PAL', origin_value='Manila', destination_value='Tacloban')

        handler = PromoHandler()
        handler.request_params = {'limit': u'10'}
        result = handler.get_promo_list()

        self.assertEquals(7, result['data']['count'])
        self.assertEquals(7, len(result['data']['promos']))

    def test_get_promo_list_more_than_limit(self):
        self.insert_sample_promos(15, airline_value='PAL', origin_value='Manila', destination_value='Tacloban')

        handler = PromoHandler()
        handler.request_params = {'limit': u'5'}
        result = handler.get_promo_list()
        
        self.assertEquals(5, result['data']['count'])
        self.assertEquals(5, len(result['data']['promos']))

    def test_get_promo_list_less_than_limit_with_date_sort(self):
        self.insert_sample_promos(7, airline_value='PAL', origin_value='Manila', destination_value='Tacloban')

        handler = PromoHandler()
        handler.request_params = {'limit': u'10', 'add_date_sort': u'DESC'}
        result = handler.get_promo_list()

        self.assertEquals(7, result['data']['count'])
        self.assertEquals(7, len(result['data']['promos']))

        for x,p in enumerate(result['data']['promos']):
            offset = 7 - (x + 1)
            self.assertEquals('Title %d' % offset, p['title'])

    def test_get_promo_list_more_than_limit_with_date_sort(self):
        self.insert_sample_promos(27, airline_value='PAL', origin_value='Manila', destination_value='Tacloban')

        handler = PromoHandler()
        handler.request_params = {'limit': u'10', 'add_date_sort': u'DESC'}
        result = handler.get_promo_list()

        self.assertEquals(10, result['data']['count'])
        self.assertEquals(10, len(result['data']['promos']))

        for x,p in enumerate(result['data']['promos']):
            offset = 27 - (x + 1)
            self.assertEquals('Title %d' % offset, p['title'])

    def test_get_promo_list_airline_filter_not_found(self):
        self.insert_sample_promos(11, airline_value='PAL', origin_value='Manila', destination_value='Tacloban')
        invalid_airline_id = Airline.add_airline('ZestAir').name()

        handler = PromoHandler()
        handler.request_params = {'limit': u'10', 'airline_id': invalid_airline_id, 'add_date_sort': u'DESC'}
        result = handler.get_promo_list()

        self.assertEqual(0, result['data']['count'])
        self.assertEqual(0, len(result['data']['promos']))

    def test_get_promo_list_airline_filter_monopoloy(self):
        ref_data1 = {}
        self.insert_sample_promos(11, airline_value='PAL', origin_value='Manila', destination_value='Tacloban', ref_data=ref_data1)

        # Insert more PAL airlines
        self.insert_sample_promos(5, airline_value='PAL', origin_value='Manila', destination_value='Tacloban', airline_key=ref_data1['airline_key'])

        # Add new airline
        new_airline_key = Airline.add_airline('ZestAir')

        # There should be no ZestAir
        handler = PromoHandler()
        handler.request_params = {'limit': u'10', 'airline_id': new_airline_key.name(), 'add_date_sort': u'DESC'}
        result = handler.get_promo_list()

        self.assertEquals(0, result['data']['count'])
        self.assertEquals(0, len(result['data']['promos']))

        # All should be PAL
        handler = PromoHandler()
        handler.request_params = {'limit': u'16', 'airline_id': ref_data1['airline_key'].name(), 'add_date_sort': u'DESC'}
        result = handler.get_promo_list()

        self.assertEquals(16, result['data']['count'])
        self.assertEquals(16, len(result['data']['promos']))

        for p in result['data']['promos']:
            self.assertEquals('PAL', p['airline']['name'])

    def test_get_promo_list_airline_filter_with_other_airline(self):
        ref_data1 = {}
        ref_data2 = {}
        self.insert_sample_promos(11, airline_value='PAL', origin_value='Manila', destination_value='Tacloban', ref_data=ref_data1)
        self.insert_sample_promos(5, airline_value='ZestAir', origin_value='Manila', destination_value='Tacloban', ref_data=ref_data2)

        # All should be PAL
        handler = PromoHandler()
        handler.request_params = {'limit': u'16', 'add_date_sort': u'DESC'}
        result = handler.get_promo_list()

        pal_count = 0
        zest_count = 0

        for p in result['data']['promos']:
            if p['airline']['name'] == 'PAL':
                pal_count += 1
            if p['airline']['name'] == 'ZestAir':
                zest_count += 1

        self.assertEquals(11, pal_count)
        self.assertEquals(5, zest_count)

    def test_get_promo_list_pagination_invalid_params(self):
        input_values = [
            # No params at all
            {
                'params': {},
                'expected': {'code': 403}
            },
            # Invalid per_page
            {
                'params': {'per_page': u''},
                'expected': {'code': 403}
            },
            {
                'params': {'per_page': u'xyz'},
                'expected': {'code': 403}
            },
            {
                'params': {'per_page': u'100.00'},
                'expected': {'code': 403}
            },
            {
                'params': {'per_page': u'0'},
                'expected': {'code': 403}
            },
            {
                'params': {'per_page': u'100'},
                'expected': {'code': 403}
            },
            # Invalid limit, no per_page
            {
                'params': {'limit': u''},
                'expected': {'code': 403}
            },
            {
                'params': {'limit': u'xyz'},
                'expected': {'code': 403}
            },
            {
                'params': {'limit': u'100.00'},
                'expected': {'code': 403}
            },
            {
                'params': {'limit': u'0'},
                'expected': {'code': 403}
            },
            {
                'params': {'limit': u'100'},
                'expected': {'code': 403}
            },
            # Invalid limit, valid per_page
            {
                'params': {'per_page': u'10', 'limit': u''},
                'expected': {'code': 403}
            },
            {
                'params': {'per_page': u'10', 'limit': u'xyz'},
                'expected': {'code': 403}
            },
            {
                'params': {'per_page': u'10', 'limit': u'100.00'},
                'expected': {'code': 403}
            },
            {
                'params': {'per_page': u'10', 'limit': u'0'},
                'expected': {'code': 403}
            },
            {
                'params': {'per_page': u'10', 'limit': u'100'},
                'expected': {'code': 403}
            },
            # No limit, per page, invalid airline_id
            {
                'params': {'airline_id': u'XYZ'},
                'expected': {'code': 403}
            },
            {
                'params': {'per_page': u'', 'airline_id': u'XYZ'},
                'expected': {'code': 403}
            },
            {
                'params': {'per_page': u'10', 'airline_id': u'XYZ'},
                'expected': {'code': 403}
            },
            {
                'params': {'per_page': u'10', 'limit': u'', 'airline_id': u'XYZ'},
                'expected': {'code': 403}
            },
            {
                'params': {'per_page': u'10', 'limit': u'10', 'airline_id': u'XYZ'},
                'expected': {'code': 403}
            },
            {
                'params': {'per_page': u'10', 'limit': u'10', 'airline_id': u'XYZ'},
                'expected': {'code': 403}
            },
            # Invalid add_date_sort, not other params
            {
                'params': {'add_date_sort': u''},
                'expected': {'code': 403}
            },
            {
                'params': {'per_page': u'', 'add_date_sort': u''},
                'expected': {'code': 403}
            },
            {
                'params': {'per_page': u'10', 'limit': u'10', 'add_date_sort': u''},
                'expected': {'code': 403}
            },
            {
                'params': {'per_page': u'10', 'limit': u'', 'add_date_sort': u''},
                'expected': {'code': 403}
            },
            {
                'params': {'per_page': u'10', 'limit': u'10', 'add_date_sort': u''},
                'expected': {'code': 403}
            },
            {
                'params': {'per_page': u'10', 'limit': u'10', 'add_date_sort': u'xyz'},
                'expected': {'code': 403}
            },
            {
                'params': {'per_page': u'10', 'limit': u'10', 'add_date_sort': u'asc'},
                'expected': {'code': 403}
            },
            {
                'params': {'per_page': u'10', 'limit': u'10', 'add_date_sort': u'desc'},
                'expected': {'code': 403}
            },
            {
                'params': {'per_page': u'10', 'limit': u'10', 'add_date_sort': u'DESC', 'airline_id': u'XYZ'},
                'expected': {'code': 403}
            },
            {
                'params': {'per_page': u'10', 'limit': u'10', 'add_date_sort': u'ASC', 'airline_id': u'XYZ'},
                'expected': {'code': 403}
            },
        ]

        for test_input in input_values:
            handler = PromoHandler()
            handler.request_params = test_input['params']
            result = handler.get_promo_list_pagination()

            for expected_key,expected_value in test_input['expected'].iteritems():
                self.assertEquals(expected_value, result[expected_key])

    def test_get_promo_list_pagination_no_results(self):
        handler = PromoHandler()
        handler.request_params = {'per_page': u'10', 'limit': u'10', 'add_date_sort': u'DESC'}
        result = handler.get_promo_list_pagination()

        self.assertEquals(0, len(result['data']))

    def test_get_promo_list_pagination_2_pages_only(self):
        ref_data1 = {}
        ref_data2 = {}
        self.insert_sample_promos(11, airline_value='PAL', origin_value='Manila', destination_value='Tacloban', ref_data=ref_data1)
        self.insert_sample_promos(5, airline_value='ZestAir', origin_value='Manila', destination_value='Tacloban', ref_data=ref_data2)

        handler = PromoHandler()
        handler.request_params = {'per_page': u'10', 'limit': u'10', 'add_date_sort': u'DESC'}
        result = handler.get_promo_list_pagination()
        self.assertEquals(2, len(result['data']))

    def test_get_promo_list_pagination_exact_10_pages(self):
        self.insert_sample_promos(100, airline_value='PAL', origin_value='Manila', destination_value='Tacloban')

        handler = PromoHandler()
        handler.request_params = {'per_page': u'10', 'limit': u'10', 'add_date_sort': u'DESC'}
        result = handler.get_promo_list_pagination()

        self.assertEquals(10, len(result['data']))

    def test_get_promo_list_pagination_more_than_10_pages(self):
        self.insert_sample_promos(101, airline_value='PAL', origin_value='Manila', destination_value='Tacloban')

        handler = PromoHandler()
        handler.request_params = {'per_page': u'10', 'limit': u'10', 'add_date_sort': u'DESC'}
        result = handler.get_promo_list_pagination()

        # Assert that the first result is title 100 (0-100)
        h1 = PromoHandler()
        h1.request_params = {'limit': u'10', 'add_date_sort': u'DESC'}
        r1 = h1.get_promo_list()
        self.assertEquals(10, len(r1['data']['promos']))
        self.assertEquals('Title 100', r1['data']['promos'][0]['title'])

        # Assert that the last result is title 1 before the last page
        h2 = PromoHandler()
        h2.request_params = {'limit': u'10', 'add_date_sort': u'DESC', 'start_cursor': result['data'][8]}
        r2 = h2.get_promo_list()
        self.assertEquals(10, len(r2['data']['promos']))
        self.assertEquals('Title 1', r2['data']['promos'][9]['title'])

        # Assert that the last last page is only 1 item with title 0
        h3 = PromoHandler()
        h3.request_params = {'limit': u'10', 'add_date_sort': u'DESC', 'start_cursor': result['data'][9]}
        r3 = h3.get_promo_list()
        self.assertEquals(1, len(r3['data']['promos']))
        self.assertEquals('Title 0', r3['data']['promos'][0]['title'])        


if __name__ == '__main__':
    unittest2.main()