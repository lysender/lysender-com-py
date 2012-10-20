import os
import string
import urllib
import yaml
import json
import webapp2
from dclab.handler.web import WebHandler

class SprintHandler(WebHandler):
    def sprint_list(self):
        self.template_params['sprint_letters'] = string.lowercase
        self.template_params['sprint_url'] = webapp2.uri_for('sprint_list', _full=True)
        self.template_params['sprint_url_encoded'] = urllib.quote_plus(self.template_params['sprint_url'])
        self.template_params['show_google_plusone'] = True
        self.template_params['show_facebook_like'] = True

        self.set_ga_tags('extras_sprint', None)
        self.render_template(os.path.join('extra', 'sprint', 'index.html'))

    def sprint_letter(self, **kwargs):
        self.template_params['sprint_letter'] = kwargs['sprint_letter']
        self.template_params['sprint_letters'] = string.lowercase
        self.template_params['sprint_url'] = webapp2.uri_for('sprint_list', _full=True)
        self.template_params['sprint_url_encoded'] = urllib.quote_plus(self.template_params['sprint_url'])
        self.template_params['show_google_plusone'] = True
        self.template_params['show_facebook_like'] = True

        # Attempt to load sprint suggestions
        config = {}
        filename = os.path.join('dclab', 'config', 'sprint', '%s.yaml' % kwargs['sprint_letter'])
        try:
            stream = file(filename, 'r')
            config = yaml.load(stream)
            stream.close()
        except IOError:
            config = {}

        page_name = 'Extras - Sprint %s' % kwargs['sprint_letter'].upper()

        # Inject head script for global sprint variables on js
        if 'adjectives' in config and 'animals' in config:
            head_script = 'var sprintAdj = %s; var sprintAnimals = %s' % (json.dumps(config['adjectives']),
                                                                          json.dumps(config['animals']))
            self.template_params['head_scripts'].append(head_script)
            self.template_params['has_list'] = True
        else:
            page_name += ' - No List Yet'

        self.template_params['scripts'].append('media/js/sprint.js')
        self.set_ga_tags('extras_sprint_letter', {'sub_section': page_name})
        self.render_template(os.path.join('extra', 'sprint', 'letter.html'))