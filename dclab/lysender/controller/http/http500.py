from dclab.lysender.controller import BaseController

class Http500Controller(BaseController):
    template_dir = 'http/http500'

    def action_index(self):
        self.template = 'index.html'