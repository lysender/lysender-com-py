from google.appengine.ext import webapp
from dclab.promoflight.model.airline import Airline
from dclab.promoflight.model.promo import Promo
from dclab.promoflight.handler.api import ApiHandler

class AirlineHandler(ApiHandler):
    """Promoflight airline request handler"""

    api_methods = {
        'get': [
            'get_airline',
            'get_airlines',
        ],
        'post': [
            'add_airline',
            'update_airline',
            'delete_airline',
        ]
    }

    def get_airline(self):
        """Returns airline information, required param: airline_id"""
        airline_id = self.get_api_param('airline_id')
        result = None

        if airline_id is not None:
            a = Airline.get_airline(airline_id)
            if a and isinstance(a, Airline) and a.key().name() == airline_id:
                result = {
                    'id': a.key().name(),
                    'name': a.name
                }

        if result is not None:
            return {'data': result}
        else:
            return {'code': 404, 'message': 'Airline not found'}

    def get_airlines(self):
        """Returns all airlines"""
        airlines = Airline.get_airlines()
        if airlines:
            result = []
            for airline in airlines:
                result.append({
                    'id': airline.key().name(),
                    'name': airline.name
                })
            return {'data': result}
        else:
            return {'code': 404, 'message': 'No airlines found'}

    
    def add_airline(self):
        """Adds an airline, required param is airline name"""
        airline_name = self.get_api_param('name')

        if airline_name is not None:
            result = Airline.add_airline(airline_name)
            if result is not None:
                k = result.name()
                return {'data': k}
            else:
                return {'code': 500, 'message': 'Add airline failed'}
        else:
            return {'code': 403, 'message': 'Invalid parameters'}

    def update_airline(self):
        """Updates airline information, required params are: airline_id, airline_name"""
        airline_id = self.get_api_param('airline_id')
        airline_name = self.get_api_param('name')

        if airline_id is not None and airline_name is not None:
            result = Airline.update_airline(airline_id, airline_name)
            if result is not None and airline_id == result.name():
                return {'data': result.name()}
            else:
                return {'code': 500, 'message': 'Update airline failed'}
        else:
            return {'code': 403, 'message': 'Invalid parameters'}

    def delete_airline(self):
        """Deletes an airline, required param: airline_id"""
        airline_id = self.get_api_param('airline_id')
        if airline_id is not None:
            from dclab.promoflight.model.promo import Promo
            result = Airline.delete_airline(airline_id, Promo)
            if result:
                return {}
            else:
                return {'code': 500, 'message': 'Delete failed'}
        else:
            return {'code': 403, 'message': 'Invalid parameters'}