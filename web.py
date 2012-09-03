import webapp2
import os

import config
from dclab.handler import web

app = webapp2.WSGIApplication(config.routes, debug=True, config=config.config)
app.error_handlers[404] = web.handle_404
app.error_handlers[500] = web.handle_500
