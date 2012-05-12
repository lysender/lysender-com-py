import datetime

from google.appengine.ext import webapp

import dclab
from dclab.promoflight.model.location import Location
from dclab.promoflight.model.airline import Airline
from dclab.promoflight.model.promo import Promo
from dclab.promoflight.handler.api import ApiHandler

class PromoHandler(ApiHandler):
    """Promoflight promo request handler"""

    api_methods = {
        'get': [
            'get_promo_detail',
            'get_latest_promos',
            'get_promo_list',
            'get_promo_list_pagination',
        ],
        'post': [
            'add_promo',
            'update_promo',
            'delete_promo',
        ]
    }

    def get_promo_detail(self):
        """Returns promo information, required param: promo_id"""
        promo_id = self.get_api_param('promo_id')
        result = None

        if promo_id is not None:
            p = Promo.get_promo(promo_id)
            if p and isinstance(p, Promo) and p.key().name() == promo_id:
                result = {
                    'id': p.key().name(),
                    'title': p.title,
                    'selling_period_start': p.selling_period_start.isoformat(),
                    'selling_period_end': p.selling_period_end.isoformat(),
                    'travel_period_start': p.travel_period_start.isoformat(),
                    'travel_period_end': p.travel_period_end.isoformat(),
                    'description': p.description
                }
                if p.airline and isinstance(p.airline, Airline):
                    result['airline'] = {
                        'id': p.airline.key().name(),
                        'name': p.airline.name
                    }

                if p.origin and isinstance(p.origin, Location):
                    result['origin'] = {
                        'id': p.origin.key().name(),
                        'name': p.origin.name
                    }                

                if p.destination and isinstance(p.destination, Location):
                    result['destination'] = {
                        'id': p.destination.key().name(),
                        'name': p.destination.name
                    }

        if result is not None:
            return {'data': result}
        else:
            return {'code': 404, 'message': 'Location not found'}
    
    def add_promo(self):
        """
        Adds a promo

        Required params are
            title
            airline_id
            origin_id
            destination_id
            selling_period_start
            selling_period_end
            travel_period_start
            travel_period_end
            description
        """
        req_params = [
            'title',
            'selling_period_start',
            'selling_period_end',
            'travel_period_start',
            'travel_period_end',
            'description'
        ]
        entity_params = {
            'airline_id': {'model_field': 'airline', 'model': Airline},
            'origin_id': {'model_field': 'origin', 'model': Location},
            'destination_id': {'model_field': 'destination', 'model': Location}
        }
        date_params = [
            'selling_period_start',
            'selling_period_end',
            'travel_period_start',
            'travel_period_end'
        ]
        data = {}
        valid_params = True
        last_message = None

        # Validate required entities
        for request_key, field_specs in entity_params.iteritems():
            request_value = self.get_api_param(request_key)
            if not request_value:
                valid_params = False
                last_message = '%s is required' % request_key
                break

            entity = field_specs['model'].get_entity(request_value)
            if entity is None:
                valid_params = False
                last_message = '%s is not a valid entity' % request_key
                break

            data[field_specs['model_field']] = entity.key()

        # Validate further all required params
        if valid_params:
            for request_key in req_params:
                request_value = self.get_api_param(request_key)
                if request_value is None:
                    valid_params = False
                    last_message = '%s is required' % request_key
                    break
                else:
                    if request_key in date_params:
                        d = dclab.get_valid_date(request_value)
                        if not d:
                            # Invlid date encountered
                            valid_params = False
                            last_message = '%s is not a valid date' % request_key
                            break
                        else:
                            data[request_key] = datetime.date(d.year, d.month, d.day)
                    else:
                        data[request_key] = request_value.strip()

        if valid_params:
            result = Promo.add_promo(data)
            if result is not None:
                return {'data': result.name()}
            else:
                return {'code': 500, 'message': 'Add promo failed'}
        else:
            message = 'Invalid parameters'
            if last_message:
                message = last_message
            return {'code': 403, 'message': message}

    def update_promo(self):
        """
        Updates a promo

        Required param
            promo_id

        Optional params are
            title
            airline_id
            origin_id
            destination_id
            selling_period_start
            selling_period_end
            travel_period_start
            travel_period_end
            description
        """
        opt_params = [
            'title',
            'selling_period_start',
            'selling_period_end',
            'travel_period_start',
            'travel_period_end',
            'description'
        ]
        entity_params = {
            'airline_id': {'model_field': 'airline', 'model': Airline},
            'origin_id': {'model_field': 'origin', 'model': Location},
            'destination_id': {'model_field': 'destination', 'model': Location}
        }
        date_params = [
            'selling_period_start',
            'selling_period_end',
            'travel_period_start',
            'travel_period_end'
        ]
        data = {}
        valid_params = True
        last_message = None

        promo_id = self.get_api_param('promo_id')
        if promo_id is None:
            valid_params = False
            last_message = 'Promo not found'

        # Validate optional entities
        if valid_params:
            for request_key, field_specs in entity_params.iteritems():
                request_value = self.get_api_param(request_key)

                if request_value:
                    entity = field_specs['model'].get_entity(request_value)

                    if entity is None:
                        valid_params = False
                        last_message = '%s is not a valid entity' % request_key
                        break

                data[field_specs['model_field']] = entity.key()

        # Validate all optional params
        if valid_params:
            for request_key in opt_params:
                request_value = self.get_api_param(request_key)
                if request_value:
                    if request_key in date_params:
                        d = dclab.get_valid_date(request_value)
                        if not d:
                            valid_params = False
                            last_message = '%s is not a valid date' % request_key
                            break
                        else:
                            data[request_key] = datetime.date(d.year, d.month, d.day)
                    else:
                        data[request_key] = request_value.strip()

        if valid_params:
            result = Promo.update_promo(promo_id, data)
            if result is not None:
                return {'data': result.name()}
            else:
                return {'code': 500, 'message': 'Update promo failed'}
        else:
            message = 'Invalid parameters'
            if last_message:
                message = last_message
            return {'code': 403, 'message': message}

    def delete_promo(self):
        """Deletes a promo, required param: promo_id"""
        promo_id = self.get_api_param('promo_id')
        if promo_id is not None:
            result = Promo.delete_promo(promo_id)
            if result:
                return {}
            else:
                return {'code': 500, 'message': 'Delete failed'}
        else:
            return self.invalid_param_return

    def get_latest_promos(self):
        """Returns latest promos"""

        result = Promo.get_latest_promos()
        return {'data': self.generate_promo_list(result)}

    def get_promo_list(self):
        """
        Returns promo list with filters and sorting

        Required params:
            limit

        Optional params:
            airline_id
            add_date_sort
            start_cursor
        """
        limit = self.get_api_param('limit')
        airline_id = self.get_api_param('airline_id')
        add_date_sort = self.get_api_param('add_date_sort')
        start_cursor = self.get_api_param('start_cursor')

        valid_params = True
        last_message = None
        airline_key = None

        params = {}

        if limit is not None:
            if isinstance(limit, unicode) and limit.isdigit() and int(limit) > 0 and int(limit) <= 20:
                limit = int(limit)
            else:
                valid_params = False
                last_message = 'Limit is invalid'
        else:
            valid_params = False
            last_message = 'Limit is invalid'

        if valid_params and airline_id is not None:
            air = Airline.get_airline(airline_id)

            if not isinstance(air, Airline):
                valid_params = False
                last_message = 'Airline is not found'
            else:
                airline_key = air.key()
                params['airline'] = airline_key

        if valid_params and add_date_sort is not None:
            if isinstance(add_date_sort, unicode):
                if add_date_sort not in ['ASC', 'DESC']:
                    valid_params = False
                    last_message = 'Date sort is invalid'
                else:
                    params['add_date_sort'] = add_date_sort
            else:
                valid_params = False
                last_message = 'Date sort is invalid'

        if valid_params and start_cursor is not None:
            if len(start_cursor) > 64:
                params['start_cursor'] = start_cursor
            else:
                valid_params = False
                last_message = 'Start cursor is invalid'            

        if valid_params:
            result = Promo.get_promo_list(limit, params)

            if isinstance(result, list):
                return {'data': self.generate_promo_list(result)}
            else:
                return {'code': 500, 'message': 'Failed to get promo listing'}
        else:
            message = self.invalid_param_return['message']
            if last_message:
                message = last_message

            return {'code': 403, 'message': message}

    def generate_promo_list(self, data):
        ret = {'count': 0, 'promos': []}

        if isinstance(data, list):
            ret['count'] = len(data)
            for row in data:
                tmp = {}
                tmp['id'] = row.key().name()
                tmp['title'] = row.title

                if getattr(row, 'airline', None) is not None and isinstance(row.airline, Airline):
                    tmp['airline'] = {
                        'id': row.airline.key().name(),
                        'name': row.airline.name
                    }

                if getattr(row, 'origin', None) is not None and isinstance(row.origin, Location):
                    tmp['origin'] = {
                        'id': row.origin.key().name(),
                        'name': row.origin.name
                    }

                if getattr(row, 'destination', None) is not None and isinstance(row.destination, Location):
                    tmp['destination'] = {
                        'id': row.destination.key().name(),
                        'name': row.destination.name
                    }

                tmp['selling_period_start'] = row.selling_period_start.strftime('%Y-%m-%d')
                tmp['selling_period_end'] = row.selling_period_end.strftime('%Y-%m-%d')
                tmp['travel_period_start'] = row.travel_period_start.strftime('%Y-%m-%d')
                tmp['travel_period_end'] = row.travel_period_end.strftime('%Y-%m-%d')
                tmp['description'] = row.description
                tmp['add_date'] = row.add_date.strftime('%Y-%m-%d %H:%M:%S')
                tmp['modefied_date'] = row.add_date.strftime('%Y-%m-%d %H:%M:%S')

                ret['promos'].append(tmp)

        return ret

    def get_promo_list_pagination(self):
        """
        Returns pagination with cursors per pages

        Required param:
            per_page
            limit

        Optional params:
            airline_id
            add_date_sort
            start_cursor
        """
        per_page = self.get_api_param('per_page')
        limit = self.get_api_param('limit')
        airline_id = self.get_api_param('airline_id')
        add_date_sort = self.get_api_param('add_date_sort')
        start_cursor = self.get_api_param('start_cursor')
        params = {}

        valid_params = False
        last_message = None

        if per_page is not None:
            if isinstance(per_page, unicode) and per_page.isdigit() and int(per_page) > 0 and int(per_page) <= 20:
                valid_params = True
                per_page = int(per_page)
            else:
                valid_params = False
                last_message = 'per_page parameter must be between 1-20'
        else:
            valid_params = False
            last_message = 'per_page parameter must be between 1-20'

        if valid_params and limit is not None:
            if isinstance(limit, unicode) and limit.isdigit() and int(limit) > 0 and int(limit) <= 20:
                valid_params = True
                limit = int(limit)
            else:
                valid_params = False
                last_message = 'limit parameter must be between 1-20'
        else:
            valid_params = False
            last_message = 'limit parameter must be between 1-20'

        # Validate optional params
        if valid_params and airline_id is not None:
            air = Airline.get_airline(airline_id)

            if not isinstance(air, Airline):
                valid_params = False
                last_message = 'Airline is not found'
            else:
                airline_key = air.key()
                params['airline'] = airline_key

        if valid_params and add_date_sort is not None:
            if isinstance(add_date_sort, unicode):
                if add_date_sort not in ['ASC', 'DESC']:
                    valid_params = False
                    last_message = 'Date sort is invalid'
                else:
                    params['add_date_sort'] = add_date_sort
            else:
                valid_params = False
                last_message = 'Date sort is invalid'

        if valid_params and start_cursor is not None:
            if len(start_cursor) > 64:
                params['start_cursor'] = start_cursor
            else:
                valid_params = False
                last_message = 'Start cursor is invalid'

        if valid_params:
            result = Promo.get_promo_cursors(per_page, limit, params)

            if isinstance(result, list):
                return {'data': result}
            else:
                return {'code': 500, 'message': 'Failed to get promo listing pagination'}
        else:
            message = self.invalid_param_return['message']
            if last_message:
                message = last_message

            return {'code': 403, 'message': message}
