import os
import config

if not config.is_initialized():
    config.initialize()

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from dclab.handler import web

def main():
    application = webapp.WSGIApplication([('/.*', web.WebHandler)], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()