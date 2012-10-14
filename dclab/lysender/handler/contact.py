import os
from dclab.handler.web import WebHandler

class ContactHandler(WebHandler):
    def get(self):
        self.set_ga_tags('contact', None)
        self.render_template(os.path.join('contact', 'index.html'))