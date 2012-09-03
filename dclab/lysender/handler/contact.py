import os
from dclab.handler.web import WebHandler

class ContactHandler(WebHandler):
    def get(self):
        self.render_template(os.path.join('contact', 'index.html'))