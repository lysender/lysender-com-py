# Base controller
from google.appengine.ext.webapp import template 

import os
import config

class BaseController:

    request = None
    response = None
    action = 'index'
    method = 'get'
    params = []
    template_values = {}
    template_dir = None
    template = None

    styles = ['/media/css/style.css']
    scripts = ['/media/js/jquery-1.6.4.min.js']

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

    def pre_dispatch(self):
        pass

    def post_dispatch(self):
        if self.template is not None and self.template_dir is not None:
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