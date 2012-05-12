import os
import config

if not config.is_initialized():
    config.initialize()

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from dclab.promoflight.handler.admin.index import IndexHandler
from dclab.promoflight.handler.admin.airline import AirlineHandler
from dclab.promoflight.handler.admin.location import LocationHandler
from dclab.promoflight.handler.admin.promo import PromoHandler
from dclab.promoflight.handler.admin.news import NewsHandler

def main():
    application = webapp.WSGIApplication([('/admin', IndexHandler),
                                         ('/admin/airline', AirlineHandler),
                                         ('/admin/location', LocationHandler),
                                         ('/admin/promo', PromoHandler),
                                         ('/admin/news', NewsHandler),
                                         ], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()