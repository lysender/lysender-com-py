import os
import webapp2
import logging
import datetime

import config

class WebHandler(webapp2.RequestHandler):
    '''Base handler for site'''

    def __init__(self, request, response):
        self.initialize(request, response)
        self.template_params = get_template_params()

    def set_ga_tags(self, index, extra):
        tags = get_page_tags(index)
        if extra:
            for k,v in extra.items():
                tags[k]['value'] = v
        if tags:
            self.template_params['has_ga_tags'] = True
            self.template_params['ga_tags'] = tags

    def render_template(self, template_file):
        template = config.jinja_environment.get_template(template_file)
        self.response.out.write(template.render(self.template_params))

def get_template_params():
    app = webapp2.get_app()
    template_params = {}
    template_params['base_url'] = webapp2.uri_for('index', _full=True)
    template_params['scripts'] = list(app.config.get('template_scripts'))
    template_params['head_scripts'] = []
    template_params['styles'] = list(app.config.get('template_styles'))
    template_params['show_google_analytics'] = app.config.get('show_google_analytics')

    # Populate current year
    template_params['current_year'] = datetime.date.today().year

    return template_params

def get_page_tags(index):
    if index in config.analytics_config:
        return config.analytics_config[index]
    return None

def handle_404(request, response, exception):
    '''Handles 404 custom page'''
    template_params = get_template_params()
    logging.exception(exception)
    requested_page = request.path

    if request.query_string:
        requested_page += '?%s' % request.query_string
        
    template_params['requested_page'] = requested_page

    template = config.jinja_environment.get_template(os.path.join('http', 'http404.html'))
    response.out.write(template.render(template_params))
    response.set_status(404)

def handle_500(request, response, exception):
    '''Handles application error custom page'''
    template_params = get_template_params()
    logging.exception(exception)
    template_params['exception_args'] = exception.args
    template = config.jinja_environment.get_template(os.path.join('http', 'http500.html'))
    response.out.write(template.render(template_params))
    response.set_status(500)
