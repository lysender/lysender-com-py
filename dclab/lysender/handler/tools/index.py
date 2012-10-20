import os
from dclab.handler.web import WebHandler

class IndexHandler(WebHandler):
    def get(self):
        self.set_ga_tags('tools', None)
        self.render_template(os.path.join('tools', 'index', 'index.html'))