import os
import urllib
from dclab.handler.web import WebHandler

class UrlencodeHandler(WebHandler):
    def get(self):
        self.template_params['styles'].extend(['media/bootstrap/css/bootstrap-responsive.min.css', 
                                               'media/css/tools.css'])
        self.template_params['scripts'].append('media/js/urlencode.js')
        self.template_params['page_urlencoded'] = urllib.quote_plus('%sextra/tools/urlencode' % self.template_params['base_url'])
        self.template_params['show_google_plusone'] = True
        self.template_params['show_facebook_like'] = True
        self.set_ga_tags('tools_urlencode', None)
        self.render_template(os.path.join('extra', 'tools', 'urlencode', 'index.html'))