from dclab.lysender.controller import BaseController

class Http404Controller(BaseController):
    template_dir = 'http/http404'

    def action_index(self):
        self.template = 'index.html'