from google.appengine.ext import webapp

from dclab.handler.rest import RestHandler

class ApiHandler(RestHandler):
    """Promoflight base API request handler"""

    api_key = '2b1dab4779f24713816502d44c40316b'