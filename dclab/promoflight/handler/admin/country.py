import os

from google.appengine.ext.webapp import util
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template 

import config

class CountryHandler(webapp.RequestHandler):
    '''Admin country page handler'''

    def get(self):
        greetings = 'this is a greeting foo'
        url = 'http://www.promoflight.info'
        url_linktext = 'this is a url link index'

        template_values = {
            'greetings': greetings,
            'url': url,
            'url_linktext': url_linktext,
        }

        path = os.path.join(config.template_dir, 'admin', 'index', 'index.html')
        self.response.out.write(template.render(path, template_values))