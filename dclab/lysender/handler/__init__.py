# Base controller
from google.appengine.ext.webapp import template 

import os
import config
import datetime

class BaseController(object):

    request = None
    response = None
    action = 'index'
    method = 'get'
    params = []
    max_param_level = {}
    template_values = {}
    template_dir = None
    template = None

    default_styles = ['/media/bootstrap/css/bootstrap.min.css', '/media/css/style.css']
    default_scripts = ['/media/js/jquery-1.6.4.min.js']

    styles = []
    scripts = []

    def __init__(self, request, response, *args, **kwargs):
        self.request = request
        self.response = response

        self.action = 'index'
        if 'action' in kwargs and kwargs['action']:
            self.action = kwargs['action']

        self.method = 'get'
        if 'method' in kwargs and kwargs['method']:
            self.method = kwargs['method']

        self.params = []
        if 'params' in kwargs and kwargs['params']:
            if isinstance(kwargs['params'], list):
                self.params = kwargs['params']

        action_max_params = 0
        if self.action in self.max_param_level:
            action_max_params = self.max_param_level[self.action]

        if len(self.params) != action_max_params:
            raise Http404Exception('Request exceed maximum parameter: %s for controller' % self.max_param_level)

        # Initialize template related variables
        self.template_values = {}
        self.styles = list(self.default_styles)
        self.scripts = list(self.default_scripts)

    def pre_dispatch(self):
        pass

    def post_dispatch(self):
        if self.template is not None and self.template_dir is not None:
            # Populate current year
            dt = datetime.date.today()
            self.template_values['current_year'] = dt.year
            
            # Populate styles and scripts
            self.template_values['styles'] = self.styles
            self.template_values['scripts'] = self.scripts

            path = os.path.join(config.template_dir, self.template_dir, self.template)
            self.response.out.write(template.render(path, self.template_values))

    def run_action(self):
        action_name = 'action_' + self.action
        if hasattr(self, action_name):
            action = getattr(self, action_name)
            action()
        else:
            raise Http404Exception('Controller action not found')

    def dispatch(self):
        self.pre_dispatch()
        self.run_action()
        self.post_dispatch()

class HttpException(Exception):
    """Http Exception"""
    pass

class Http404Exception(HttpException):
    """Http 404 exception"""
    pass

class Http500Exception(HttpException):
    """Http 500 exception"""
    pass