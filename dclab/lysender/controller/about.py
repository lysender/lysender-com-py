import datetime

from dclab.lysender.controller import BaseController

class AboutController(BaseController):

    template_dir = 'about'

    def action_index(self):
        self.template = 'index.html'

        # Compute my age
        birth_date = datetime.date(1985, 8, 8)
        today = datetime.date.today()
        age = today.year - birth_date.year

        if today.month < birth_date.month:
            age -= 1
        elif today.month == birth_date.month and today.day < birth_date.day:
            age -= 1

        self.template_values['age'] = age
