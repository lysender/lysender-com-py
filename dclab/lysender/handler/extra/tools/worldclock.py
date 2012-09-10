import os
import urllib
import datetime
import json
import pytz
from dclab.handler.web import WebHandler

import webapp2
from google.appengine.api import memcache

class WorldclockHandler(WebHandler):

    def set_shared_params(self, lookup, tz_group):
        sorted_keys = tz_group['ALL'].keys()
        sorted_keys.sort()
        self.template_params['timezones_keys'] = sorted_keys
        self.template_params['timezones'] = tz_group['ALL']
        self.template_params['head_scripts'].append('var tzlist = %s' % json.dumps(tz_group, sort_keys=True))
        self.template_params['styles'].extend(['media/bootstrap/css/bootstrap-responsive.min.css', 
                                               'media/css/tools.css'])
        self.template_params['scripts'].extend(['media/js/json2_min.js',
                                                'media/js/cookiegroup.js',
                                                'media/js/worldclock.js'])
        self.template_params['page_urlencoded'] = urllib.quote_plus('%sextra/tools/worldclock' % self.template_params['base_url'])
        self.template_params['show_google_plusone'] = True
        self.template_params['show_facebook_like'] = True
        self.render_template(os.path.join('extra', 'tools', 'worldclock', 'index.html'))        

    def get(self):
        lookup = self.get_timezone_offset_lookup()
        tz_group = self.get_timezones_by_region(lookup)

        self.template_params['page_title'] = 'Extras - Tools - World Clock'
        self.template_params['page_desc'] = 'Extras - Tools - World Clock'

        self.set_shared_params(lookup, tz_group)

    def specific_timezone(self, **kwargs):
        params = ['ident1', 'ident2', 'ident3']
        url_parts = []

        for param in params:
            if param in kwargs:
                url_parts.append(kwargs[param])

        lookup = self.get_timezone_offset_lookup()
        tz_group = self.get_timezones_by_region(lookup)

        selected_timezone = '/'.join(url_parts)
        formatted_timezone = None
        if selected_timezone in lookup:
            formatted_timezone = selected_timezone.replace('_', ' ')

        self.template_params['formatted_timezone'] = formatted_timezone
        self.template_params['selected_timezone'] = selected_timezone
        self.template_params['page_title'] = '%s - World Clock' % formatted_timezone
        self.template_params['page_desc'] = '%s - World Clock' % formatted_timezone
        self.template_params['head_scripts'].append('var selected_timezone = %s' % json.dumps(selected_timezone))
        self.set_shared_params(lookup, tz_group)

    def get_timezone_offset_lookup(self):
        tz_offsets = memcache.get('worldclock_offset_lookup')
        if not tz_offsets:
            webapp2.abort(500)
        return tz_offsets

    def get_timezones_by_region(self, offset_lookup):
        tz_groups = {}

        for tz in pytz.common_timezones:
            country = tz.split('/', 1)[0]
            offset = 0
            if tz in offset_lookup:
                offset = offset_lookup[tz]
            if country in tz_groups:
                tz_groups[country][tz] = offset
            else:
                tz_groups[country] = {tz:offset}

        # Set all timezones group
        tz_groups['ALL'] = {}
        for atz in pytz.all_timezones:
            offset = 0
            if atz in offset_lookup:
                offset = offset_lookup[atz]
            tz_groups['ALL'][atz] = offset

        return tz_groups