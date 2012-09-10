import os
import webapp2
import jinja2

routes = [webapp2.Route(r'/', handler='dclab.lysender.handler.index.IndexHandler', name='index'),
          webapp2.Route(r'/about', handler='dclab.lysender.handler.about.AboutHandler', name='about'),
          webapp2.Route(r'/contact', handler='dclab.lysender.handler.contact.ContactHandler', name='contact'),
          webapp2.Route(r'/projects', handler='dclab.lysender.handler.projects.ProjectsHandler:projects_list', name='projects_list', methods=['GET']),
          webapp2.Route(r'/projects/chrome-time-in-time-out', handler='dclab.lysender.handler.projects.ProjectsHandler:projects_chrometito', name='projects_chrometito', methods=['GET']),
          webapp2.Route(r'/extra', handler='dclab.lysender.handler.extra.index.IndexHandler', name='extra_index'),
          webapp2.Route(r'/extra/sprint', handler='dclab.lysender.handler.extra.sprint.SprintHandler:sprint_list', name='sprint_list', methods=['GET']),
          webapp2.Route(r'/extra/sprint/<sprint_letter:[a-z]>', handler='dclab.lysender.handler.extra.sprint.SprintHandler:sprint_letter', name='sprint_letter', methods=['GET']),
          webapp2.Route(r'/extra/tools', handler='dclab.lysender.handler.extra.tools.index.IndexHandler', name='tools_index'),
          webapp2.Route(r'/extra/tools/base64', handler='dclab.lysender.handler.extra.tools.base64.Base64Handler', name='tools_base64'),
          webapp2.Route(r'/extra/tools/urlencode', handler='dclab.lysender.handler.extra.tools.urlencode.UrlencodeHandler', name='tools_urlencode'),
          webapp2.Route(r'/extra/tools/sumfirstcol', handler='dclab.lysender.handler.extra.tools.sumfirstcol.SumfirstcolHandler', name='tools_sumfirstcol'),
          webapp2.Route(r'/extra/tools/worldclock', handler='dclab.lysender.handler.extra.tools.worldclock.WorldclockHandler', name='tools_worldclock'),
          webapp2.Route(r'/extra/tools/worldclock/<ident1:[-+0-9a-zA-Z_]+>', handler='dclab.lysender.handler.extra.tools.worldclock.WorldclockHandler:specific_timezone', name='tools_worldclock_selected', methods=['GET']),
          webapp2.Route(r'/extra/tools/worldclock/<ident1:[-+0-9a-zA-Z_]+>/<ident2:[-+0-9a-zA-Z_]+>', handler='dclab.lysender.handler.extra.tools.worldclock.WorldclockHandler:specific_timezone', name='tools_worldclock_selected', methods=['GET']),
          webapp2.Route(r'/extra/tools/worldclock/<ident1:[-+0-9a-zA-Z_]+>/<ident2:[-+0-9a-zA-Z_]+>/<ident3:[-+0-9a-zA-Z_]+>', handler='dclab.lysender.handler.extra.tools.worldclock.WorldclockHandler:specific_timezone', name='tools_worldclock_selected', methods=['GET']),
          webapp2.Route(r'/sitemap.xml', handler='dclab.lysender.handler.sitemap.IndexHandler', name='sitemap'),
          webapp2.Route(r'/task/tzupdate', handler='dclab.lysender.handler.task.tzupdate.IndexHandler', name='task_tzupdate')]

template_dir = 'templates'
in_production = True


if os.environ['SERVER_SOFTWARE'].startswith('Dev'):
    in_production = False

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), template_dir)))

config = {
    'template_dir': template_dir,
    'template_styles': ['media/bootstrap/css/bootstrap.min.css', 'media/css/style.css'],
    'template_scripts': ['media/js/jquery-1.6.4.min.js'],
    'jinja_environment': jinja_environment,
    'show_google_analytics': in_production,
}
