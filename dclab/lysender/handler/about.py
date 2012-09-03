import os
import datetime
from dclab.handler.web import WebHandler

class AboutHandler(WebHandler):
    def get(self):
        # Compute my age
        birth_date = datetime.date(1985, 8, 8)
        today = datetime.date.today()
        age = today.year - birth_date.year

        if today.month < birth_date.month:
            age -= 1
        elif today.month == birth_date.month and today.day < birth_date.day:
            age -= 1

        self.template_params['age'] = age
        self.render_template(os.path.join('about', 'index.html'))