import os

project_dir = None
template_dir = None
initialized = False

controller_dirs = ['admin']

def initialize():
    global initialized

    if not initialized:
        initialized = True
        init_paths()
        init_django()

def init_paths():
    global project_dir
    global template_dir
    
    base_path = os.path.dirname(__file__)
    project_dir = base_path
    template_dir = os.path.join(base_path, 'templates')

def init_django():
    # Must set this env var before importing any part of Django
    # 'project' is the name of the project created with django-admin.py
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    from google.appengine.dist import use_library
    use_library('django', '1.2')

    # Force Django to reload its settings.
    from django.conf import settings

    # Not sure why this works, but it fixes the templates.
    settings.configure(INSTALLED_APPS=('nothing',))

def is_initialized():
    return initialized