from dclab.lysender.controller import BaseController

class IndexController(BaseController):

    template_dir = 'index'

    def action_index(self):
        self.template = 'index.html'