import os
import string
import urllib
import yaml
import json
import webapp2
from dclab.handler.web import WebHandler

class RedirectHandler(WebHandler):
    def tools_index(self):
        self.redirect(webapp2.uri_for('tools_index', _full=True), True)

    def tools_nonindex(self, **kwargs):
        redirect_url = '%stools/%s' % (webapp2.uri_for('index', _full=True), kwargs['ident1'])
        self.redirect(redirect_url, True)
