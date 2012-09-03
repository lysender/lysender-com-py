import os
import webapp2
import urllib
from dclab.handler.web import WebHandler

class SumfirstcolHandler(WebHandler):
    def get(self):
        page_url = webapp2.uri_for('tools_sumfirstcol', _full=True)
        self.template_params['page_urlencoded'] = urllib.quote_plus(page_url)
        self.template_params['page_url'] = page_url
        self.template_params['scripts'].append('media/js/sumfirstcol.js')
        self.template_params['styles'].extend(['media/bootstrap/css/bootstrap-responsive.min.css',
                                               'media/css/tools.css'])
        self.template_params['show_google_plusone'] = True
        self.template_params['show_facebook_like'] = True
        self.render_template(os.path.join('extra', 'tools', 'sumfirstcol', 'index.html'))