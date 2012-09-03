from dclab.lysender.controller import BaseController

class Http404Controller(BaseController):
    template_dir = 'http/http404'

    def action_index(self):
        self.template = 'index.html'
        requested_page = self.request.path

        if self.request.query_string:
            requested_page += '?%s' % self.request.query_string
            
        self.template_values['requested_page'] = requested_page