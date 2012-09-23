import os
import pytz
import datetime
from dclab.handler.web import WebHandler
from google.appengine.api import memcache

class IndexHandler(WebHandler):
    def get(self):
        self.update_timezone_offset_lookup()

    def update_timezone_offset_lookup(self):
        tz_list = pytz.all_timezones
        tz_offsets = {}
        d = datetime.datetime.now()

        for tz in tz_list:
            offset = 0
            try:
                t = pytz.timezone(tz)
                offset = int(t.utcoffset(d).total_seconds())
            except pytz.exceptions.UnknownTimeZoneError:
                offset = 0
            tz_offsets[tz] = offset
        memcache.set('worldclock_offset_lookup', tz_offsets, 86400)