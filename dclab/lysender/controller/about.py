from dclab.lysender.controller import BaseController

class AboutController(BaseController):

    template_dir = 'about'

    def action_index(self):
        self.template = 'index.html'