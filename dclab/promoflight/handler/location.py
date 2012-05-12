from google.appengine.ext import webapp

from dclab.promoflight.model.location import Location
from dclab.promoflight.model.promo import Promo
from dclab.promoflight.handler.api import ApiHandler

class LocationHandler(ApiHandler):
    """Promoflight location request handler"""

    api_methods = {
        'get': [
            'get_location',
            'get_locations',
        ],
        'post': [
            'add_location',
            'update_location',
            'delete_location',
        ]
    }

    def get_location(self):
        """Returns location information, required param: location_id"""
        location_id = self.get_api_param('location_id')
        result = None

        if location_id is not None:
            loc = Location.get_location(location_id)
            if loc and isinstance(loc, Location) and loc.key().name() == location_id:
                result = {
                    'id': loc.key().name(),
                    'name': loc.name
                }

        if result is not None:
            return {'data': result}
        else:
            return {'code': 404, 'message': 'Location not found'}

    def get_locations(self):
        """Returns all locations"""
        locations = Location.get_locations()
        if locations:
            result = []
            for loc in locations:
                result.append({
                    'id': loc.key().name(),
                    'name': loc.name
                })
            return {'data': result}
        else:
            return {'code': 404, 'message': 'No locations found'}
    
    def add_location(self):
        """Adds a location, required param is location name"""
        location_name = self.get_api_param('name')

        if location_name is not None and location_name:
            result = Location.add_location(location_name)
            if result is not None:
                k = result.name()
                return {'data': k}
            else:
                return {'code': 500, 'message': 'Add location failed'}
        else:
            return {'code': 403, 'message': 'Invalid parameters'}

    def update_location(self):
        """Updates location information, required params are: location_id, location name"""
        location_id = self.get_api_param('location_id')
        location_name = self.get_api_param('name')

        if location_id is not None and location_name is not None:
            result = Location.update_location(location_id, location_name)
            if result is not None and location_id == result.name():
                return {'data': result.name()}
            else:
                return {'code': 500, 'message': 'Update location failed'}
        else:
            return {'code': 403, 'message': 'Invalid parameters'}

    def delete_location(self):
        """Deletes an location, required param: location_id"""
        location_id = self.get_api_param('location_id')
        if location_id is not None:
            from dclab.promoflight.model.promo import Promo
            result = Location.delete_location(location_id, Promo)
            if result:
                return {}
            else:
                return {'code': 500, 'message': 'Delete failed'}
        else:
            return {'code': 403, 'message': 'Invalid parameters'}