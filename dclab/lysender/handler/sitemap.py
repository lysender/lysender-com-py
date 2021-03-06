import os
import yaml
from dclab.handler.web import WebHandler
from google.appengine.api import memcache

class IndexHandler(WebHandler):
    def get(self):
        # Attempt to load sprint suggestions
        config = {}
        filename = os.path.join('dclab', 'config', 'sitemap.yaml')
        try:
            stream = file(filename, 'r')
            config = yaml.load(stream)
            stream.close()
        except IOError:
            config = {}

        # Inject head script for global sprint variables on js
        if 'monthly' in config and 'weekly' in config:
            self.template_params['sitemap_basic'] = config

        timezones_lookup = memcache.get('worldclock_offset_lookup')
        if timezones_lookup:
            self.template_params['sitemap_worldclock'] = timezones_lookup.keys()

        self.response.headers['Content-Type'] = 'application/xml'
        self.render_template(os.path.join('sitemap', 'index.xml'))