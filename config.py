import os
import webapp2
import jinja2
import dclab

routes = [webapp2.Route(r'/', handler='dclab.lysender.handler.index.IndexHandler', name='index'),
          webapp2.Route(r'/about', handler='dclab.lysender.handler.about.AboutHandler', name='about'),
          webapp2.Route(r'/contact', handler='dclab.lysender.handler.contact.ContactHandler', name='contact'),
          webapp2.Route(r'/projects', handler='dclab.lysender.handler.projects.ProjectsHandler:projects_list', name='projects_list', methods=['GET']),
          webapp2.Route(r'/projects/chrome-time-in-time-out', handler='dclab.lysender.handler.projects.ProjectsHandler:projects_chrometito', name='projects_chrometito', methods=['GET']),
          webapp2.Route(r'/extra', handler='dclab.lysender.handler.extra.index.IndexHandler', name='extra_index'),
          webapp2.Route(r'/extra/sprint', handler='dclab.lysender.handler.extra.sprint.SprintHandler:sprint_list', name='sprint_list', methods=['GET']),
          webapp2.Route(r'/extra/sprint/<sprint_letter:[a-z]>', handler='dclab.lysender.handler.extra.sprint.SprintHandler:sprint_letter', name='sprint_letter', methods=['GET']),
          webapp2.Route(r'/extra/tools/<ident1:[-+0-9a-zA-Z_/]+>', handler='dclab.lysender.handler.extra.redirect.RedirectHandler:tools_nonindex', name='redir_tools_nonindex', methods=['GET']),
          webapp2.Route(r'/extra/tools/', handler='dclab.lysender.handler.extra.redirect.RedirectHandler:tools_index', name='redir_tools_index', methods=['GET']),
          webapp2.Route(r'/extra/tools', handler='dclab.lysender.handler.extra.redirect.RedirectHandler:tools_index', name='redir_tools_index2', methods=['GET']),
          webapp2.Route(r'/tools', handler='dclab.lysender.handler.tools.index.IndexHandler', name='tools_index'),
          webapp2.Route(r'/tools/base64', handler='dclab.lysender.handler.tools.base64.Base64Handler', name='tools_base64'),
          webapp2.Route(r'/tools/urlencode', handler='dclab.lysender.handler.tools.urlencode.UrlencodeHandler', name='tools_urlencode'),
          webapp2.Route(r'/tools/sumfirstcol', handler='dclab.lysender.handler.tools.sumfirstcol.SumfirstcolHandler', name='tools_sumfirstcol'),
          webapp2.Route(r'/tools/worldclock', handler='dclab.lysender.handler.tools.worldclock.WorldclockHandler', name='tools_worldclock'),
          webapp2.Route(r'/tools/worldclock/<ident1:[-+0-9a-zA-Z_]+>', handler='dclab.lysender.handler.tools.worldclock.WorldclockHandler:specific_timezone', name='tools_worldclock_selected', methods=['GET']),
          webapp2.Route(r'/tools/worldclock/<ident1:[-+0-9a-zA-Z_]+>/<ident2:[-+0-9a-zA-Z_]+>', handler='dclab.lysender.handler.tools.worldclock.WorldclockHandler:specific_timezone', name='tools_worldclock_selected', methods=['GET']),
          webapp2.Route(r'/tools/worldclock/<ident1:[-+0-9a-zA-Z_]+>/<ident2:[-+0-9a-zA-Z_]+>/<ident3:[-+0-9a-zA-Z_]+>', handler='dclab.lysender.handler.tools.worldclock.WorldclockHandler:specific_timezone', name='tools_worldclock_selected', methods=['GET']),
          webapp2.Route(r'/sitemap.xml', handler='dclab.lysender.handler.sitemap.IndexHandler', name='sitemap'),
          webapp2.Route(r'/task/tzupdate', handler='dclab.lysender.handler.task.tzupdate.IndexHandler', name='task_tzupdate')]

app_version = '2.3.0'
template_dir = 'templates'
in_production = True
analytics_config = {}

if os.environ['SERVER_SOFTWARE'].startswith('Dev'):
    in_production = False

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), template_dir)))

analytics_config = dclab.get_yaml_config('analytics.yaml')

config = {
    'template_dir': template_dir,
    'template_styles': ['media/bootstrap/css/bootstrap.min.css', 'media/css/style.css'],
    'template_scripts': ['media/js/jquery-1.8.2.min.js', 'media/js/analytics.js'],
    'jinja_environment': jinja_environment,
    'show_google_analytics': True,
    'analytics_config': analytics_config,
    'cache_buster': '?v=' + app_version
}
