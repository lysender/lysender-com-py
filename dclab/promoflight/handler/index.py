import os

from google.appengine.ext.webapp import template 

import config

class IndexHandler(webapp.RequestHandler):
    '''Index page handler'''

    def get(self):
        greetings = 'this is a greeting'
        url = 'http://www.promoflight.info'
        url_linktext = 'this is a url link text'

        template_values = {
            'greetings': greetings,
            'url': url,
            'url_linktext': url_linktext,
        }

        path = os.path.join(config.template_dir, 'index', 'index.html')
        self.response.out.write(template.render(path, template_values))