import os

# Google App Engine imports.
from google.appengine.ext.webapp import util
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template 

import config

class NewsHandler(webapp.RequestHandler):
    '''Admin index page handler'''

    def get(self):
        greetings = 'this is a greeting news'
        url = 'http://www.promoflight.info'
        url_linktext = 'this is a url link news'

        template_values = {
            'greetings': greetings,
            'url': url,
            'url_linktext': url_linktext,
        }

        path = os.path.join(config.template_dir, 'admin', 'index', 'index.html')
        self.response.out.write(template.render(path, template_values))