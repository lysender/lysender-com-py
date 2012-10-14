import os
import dclab
from dclab.handler.web import WebHandler

class IndexHandler(WebHandler):
    def get(self):
        self.set_ga_tags('index', None)
        self.render_template(os.path.join('index', 'index.html'))