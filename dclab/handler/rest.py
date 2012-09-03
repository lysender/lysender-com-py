import hashlib
import hmac
import simplejson as json

import webapp2

def generate_signature(key, parameters, sig_key='sig'):
    """Generates signature based on the passed key and parameters"""

    keys = parameters.keys()
    keys.sort()
    msg = ''

    for k in keys:
        if k != sig_key:
            msg += k + parameters[k]

    return hmac.new(key, msg, hashlib.sha256).hexdigest()

class RestHandler(webapp2.RequestHandler):
    """
    REST handler for rest requests accross the cluster

    /api/module_name?action=do_stuff&param1=value1&param2=value2&sig=blah
    """

    api_methods = {
        'get': [],
        'post': [],
        'put': [],
        'delete': []
    }

    api_key = None
    request_action = None
    request_params = {}

    invalid_param_return = {'code': 403, 'message': 'Invalid parameters'}

    def is_action_valid(self, method, action):
        """
        Returns True if and only if the action is valid for a method
        and is a valid handler method
        """
        if method in self.api_methods:
            if action in self.api_methods[method]:
                if getattr(self, action, None):
                    return True

        return False

    def is_key_valid(self, key):
        """
        Returns true if the supplied key is valid based from the validator source
        Let the child classes define the key hard coded
        """
        return self.api_key == key

    def get_api_action(self, parameters):
        """Returns the action name for the api request"""
        if 'action' in parameters:
            return parameters['action']

        return None

    def get_api_params(self):
        """Returns all request parameters from request object"""
        keys = self.request.arguments()
        data = {}

        for k in keys:
            data[k] = self.request.get(k)

        return data

    def get_api_param(self, param, default=None):
        """Returns the value of an api param set in self.request_params"""
        if param in self.request_params:
            return self.request_params[param]
        return default

    def init_action(self, method):
        """Initialize the requested action with loads of validations"""
        self.request_params = self.get_api_params()
        self.request_action = self.get_api_action(self.request_params)

        valid = False
        key = self.get_api_param('api_key')
        sig = self.get_api_param('sig')

        if key and self.is_key_valid(key) and sig == generate_signature(key, self.request_params):
            if self.is_action_valid(method, self.request_action):
                return True

        return False

    def do_action(self, method):
        """Runs the api request action"""
        if self.init_action(method):
            action = getattr(self, self.request_action)
            return action()

        return False

    def generate_response(self, data):
        """
        Response is a dictionary with the following format

        response = {
            code: code,
            message: str,
            data: stuff
        }
        """
        if 'code' not in data:
            data['code'] = 200
        if 'message' not in data:
            data['message'] = 'Success'

        return data

    def get(self):
        """Default get response"""
        self.response.headers['Content-Type'] = 'application/json'
        result = self.do_action('get')

        if result:
            self.response.out.write(json.dumps(self.generate_response(result)))
        else:
            self.response.out.write(json.dumps(
                self.generate_response(self.invalid_param_return)
            ))

    def post(self):
        """Default post response"""
        self.response.headers['Content-Type'] = 'application/json'
        result = self.do_action('post')

        if result:
            self.response.out.write(json.dumps(self.generate_response(result)))
        else:
            self.response.out.write(json.dumps(
                self.generate_response(self.invalid_param_return)
            ))