import os
import datetime
from dclab.handler.web import WebHandler

class ProjectsHandler(WebHandler):
    def projects_list(self):
        self.template_params['styles'].extend(['media/css/jquery.lightbox-0.5.css'])
        self.template_params['scripts'].extend([
            'media/js/jquery.lightbox-0.5.min.js',
            'media/js/project.js'
        ])

        self.template_params['project_images'] = {
            'techtuit': [
                'techtuit-main-menu.png',
                'techtuit-import-excel.png',
                'techtuit-shipment-mp3.png'
            ],
            'rajahtours': [
                'control-center-profiles.png',
                'control-center-rates.png',
                'control-center-vehicles.png'
            ],
            'daito': [
                'main-menu.png',
                'search-form-1.png',
                'entry-form-1.png',
                'entry-form-2.png'
            ],
            'manken': [
                'main-page.png',
                'list-page-1.png',
                'list-page-2.png',
                'mapping.png'
            ]       
        }
        self.render_template(os.path.join('projects', 'index.html'))

    def projects_chrometito(self):
        self.template_params['styles'].extend(['media/css/jquery.lightbox-0.5.css'])
        self.template_params['scripts'].extend([
            'media/js/jquery.lightbox-0.5.min.js',
            'media/js/project.js'
        ])

        self.template_params['project_images'] = {
            'chrome-tito': [
                'chrome-tito-notification.png',
                'chrome-tito-option-page.png',
            ]
        }

        self.render_template(os.path.join('projects', 'chrometito.html'))
