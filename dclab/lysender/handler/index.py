import os
from dclab.handler.web import WebHandler

class IndexHandler(WebHandler):
    def get(self):
        self.render_template(os.path.join('index', 'index.html'))