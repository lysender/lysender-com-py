import os
from dclab.handler.web import WebHandler

class ContactHandler(WebHandler):
    def get(self):
        self.render_template(os.path.join('contact', 'index.html'))

class ExtraController(BaseController):

    template_dir = 'extra'
    max_param_level = {
        'sprint': 1
    }

    def action_index(self):
        self.template = 'index.html'

    def action_sprint(self):
        self.template = 'sprint.html'
        self.template_values['sprint_letters'] = string.lowercase        
        self.template_values['sprint_url'] = '%s/extra/sprint' % config.server_url

        letter = None
        title_extra = None
        if len(self.params) == 1:
            letter = self.params[0]

        if letter:
            self.template_values['sprint_letter'] = letter
        # if ($letter)
        # {
        #   $title_extra = ' - Sprint '.strtoupper($letter);
        #   $this->view->letter = $letter;
        #   $config = Kohana::$config->load('sprint/'.$letter);

        #   if ( ! empty($config->adjectives) && ! empty($config->animals))
        #   {
        #       $this->template->head_scripts = 'var sprintAdj = '.json_encode($config->adjectives)
        #           .'; var sprintAnimals = '.json_encode($config->animals).';';

        #       $this->view->has_list = TRUE;
        #   }
        #   else
        #   {
        #       $this->view->has_list = FALSE;
        #   }
        # }

        # $this->template->title = 'Sprint Name Generator'.$title_extra;
        # $this->template->description = 'Extras - Sprint Name Generator'.$title_extra;
        # $this->template->keywords = 'extras, sprint, name, generator';
        # $this->template->scripts[] = $this->asset->asset_url('/media/js/sprint.js');
        # $this->template->styles[$this->asset->asset_url('/media/css/tools.css')] = 'screen, projection';
        # $this->template->show_google_plusone = true;
        # $this->template->show_facebook_like = true;
        self.styles.append('/media/css/tools.css')
        self.scripts.append('/media/js/sprint.js')

        self.template_values['show_google_plusone'] = True
        self.template_values['show_facebook_like'] = True
