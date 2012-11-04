import os
import validatish

import dclab
from google.appengine.api import mail
from dclab.handler.web import WebHandler

class ContactHandler(WebHandler):
    def get(self):
        token = dclab.generate_uuid()
        self.set_session_var('token', token)
        self.template_params['token'] = token
        self.template_params['scripts'].extend(['media/js/jquery.validate.min.js', 'media/js/contact.js'])
        self.set_ga_tags('contact', None)
        self.render_template(os.path.join('contact', 'index.html'))

    def post(self):
        name = self.request.get('name', None)
        email = self.request.get('email', None)
        message = self.request.get('message', None)
        token = self.request.get('token', None)

        try:
            self.process_message(name, email, message, token)
        except validatish.Invalid as e:
            self.template_params['error_messages'] = e.message

        self.template_params['name'] = name
        self.template_params['email'] = email
        self.template_params['message'] = message
        self.template_params['posted'] = True

        # Generate new token
        new_token = dclab.generate_uuid()
        self.set_session_var('token', new_token)
        self.template_params['token'] = new_token

        self.template_params['scripts'].extend(['media/js/jquery.validate.min.js', 'media/js/contact.js'])
        self.set_ga_tags('contact', None)
        self.render_template(os.path.join('contact', 'index.html'))

    def validate_post(self, name, email, message, token):
        session_token = self.get_session_var('token')
        messages = {}
        field_validators = {
            'name': [
                ['is_required', name, {
                    'required': 'Name is required'
                }],
                ['has_length', name, 2, 100, {
                    'between': 'Enter a valid name',
                    'fewer-than': 'Name is too short',
                    'more-than': 'Name is too long',
                }],
            ],
            'email': [
                ['is_required', email, {
                    'required': 'Email is required'
                }],
                ['has_length', email, 10, 100, {
                    'between': 'Enter a valid email',
                    'fewer-than': 'Email is too short',
                    'more-than': 'Email is too long',
                }],
                ['is_email', email, {
                    'type-string': 'Enter a valid email',
                    'contain-at': 'Enter a valid email',
                    'username-incorrect': 'Enter a valid email',
                    'domain-incorrect': 'Enter a valid email',
                }],
            ],
            'message': [
                ['is_required', message, {
                    'required': 'Message is required'
                }],
                ['has_length', message, 10, 500, {
                    'between': 'Enter a valid message',
                    'fewer-than': 'Message is too short',
                    'more-than': 'Message is too long',
                }],
            ],
            'token': [
                ['is_required', token, {
                    'required': 'The form was not submitted properly, try again'
                }],
                ['is_equal', token, session_token, {
                    'incorrect': 'The form was not submitted properly, try again'
                }]
            ]
        }

        # Call all validators and collect error messages
        for field,validators in field_validators.items():
            # Only get 1 error per field
            try:
                for v in validators:
                    method = v[0]
                    args = v[1:]
                    fn = getattr(validatish.validate, method)
                    fn(*args)
            except validatish.Invalid as e:
                messages[field] = e.message

        # If can haz messages, throw a big exception
        if len(messages):
            raise validatish.Invalid(messages)

        # Otherwise all is good
        return True

    def process_message(self, name, email, message, token):
        contact_config = dclab.get_yaml_config('contact.yaml')
        self.validate_post(name, email, message, token)

        sender_line = '%s <%s>' % (contact_config['sender_name'], contact_config['sender_email'])
        receiver_line = '%s <%s>' % (contact_config['receiver_name'], contact_config['receiver_email'])

        # Send the email now
        msg = mail.EmailMessage(sender=sender_line,
                                    subject=contact_config['subject_line'])

        msg.to = receiver_line
        msg.body = contact_config['message_body'] % (name, name, email, message)

        msg.send()
