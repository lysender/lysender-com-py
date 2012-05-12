from google.appengine.ext import webapp
import re

from dclab.lysender.controller.http import http404
from dclab.lysender.controller.http import http500
from dclab.lysender.controller import Http404Exception
from dclab.lysender.controller import Http500Exception

class WebHandler(webapp.RequestHandler):
    """
    Web handler for web/http requests accross the cluster

    /foo/bar/baz
    """

    def get_app_controller(self, request, response, method):
        """Returns the app controller for that matches the request's path"""
        path = self.request.path.strip('/')
        app_controller = None

        if len(path) < 100 and self.is_valid_url_pattern(path):
            bpath = self.get_controller_path(self.request.path, [])
            
            if 'path' in bpath and 'controller' in bpath:
                modpath = '.'.join(bpath['path'])
                controller = bpath['controller']
                action = None
                params = []

                if 'action' in bpath:
                    action = bpath['action']

                if 'params' in bpath:
                    params = bpath['params']

                try:
                    mod = __import__(modpath, globals(), locals(), [controller], -1)
                    the_class = getattr(mod, controller.title() + 'Controller')
                    app_controller = the_class(request, response, action=action, method=method, params=[])
                except ImportError:
                    raise Http404Exception('Unable to import controller')

        if app_controller is None:
            raise Http404Exception('Unable to import controller')

        return app_controller

    def is_valid_url_pattern(self, url):
        """Returns true when url is valid"""
        chunks = url.split('/')
        ret = True
        valid_pattern = '[a-z]+[a-z0-9_]+'
        
        for c in chunks:
            if c:
                if not re.match(valid_pattern, c):
                    ret = False
                    break

        return ret

    def get_controller_path(self, path, admin_dirs):
        """Returns the path for importing modules for the controller"""
        ret = {'path': ['dclab', 'lysender', 'controller']}
        cpath = ''

        if path == '' or path == '/':
            ret['path'].append('index')
            ret['controller'] = 'index'
        else:
            chunks = path.strip('/').split('/')
            clen = len(chunks)

            if clen > 0:
                if len(chunks[0]) > 0:
                    # Check if the first chunk is a directory
                    if chunks[0] in admin_dirs:
                        ret['path'].append(chunks[0])

                        if clen > 1:
                            chunks = chunks[1:]

                    bpath = self.get_beyond_directory(chunks)
                    if 'controller' in bpath:
                        ret['path'].append(bpath['controller'])
                        ret['controller'] = bpath['controller']
                        if 'action' in bpath:
                            ret['action'] = bpath['action']
                            if 'params' in bpath:
                                ret['params'] = bpath['params']

        # The final path, action and params
        return ret

    def get_beyond_directory(self, chunks):
        """Returns the values of url parts"""
        ret = {}
        clen = len(chunks)

        if clen > 0:
            ret['controller'] = chunks[0]
            if clen > 1:
                ret['action'] = chunks[1]
                if clen > 2:
                    ret['params'] = chunks[2:]

        return ret

    def dispatch(self, method):
        """Default {method} response"""

        self.action = None
        self.params = []
        self.controller = None
        self.directory = None

        try:
            self.get_app_controller(self.request, self.response, method).dispatch()
        except Http404Exception:
            controller = http404.Http404Controller(self.request, self.response, action='index', method=method, params=[])
            controller.dispatch()
        except Http500Exception:
            controller = http500.Http500Controller(self.request, self.response, action='index', method=method, params=[])
            controller.dispatch()

    def get(self):
        """Default get response"""
        self.dispatch('get')

    def post(self):
        """Default post response"""
        self.dispatch('post')