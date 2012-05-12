from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

from dclab.promoflight.handler.airline import AirlineHandler
from dclab.promoflight.handler.location import LocationHandler
from dclab.promoflight.handler.promo import PromoHandler

def main():
    application = webapp.WSGIApplication([('/promoflight/airline', AirlineHandler),
                                          ('/promoflight/location', LocationHandler),
                                          ('/promoflight/promo', PromoHandler)
                                         ], debug=True)
    util.run_wsgi_app(application)

if __name__ == '__main__':
    main()
