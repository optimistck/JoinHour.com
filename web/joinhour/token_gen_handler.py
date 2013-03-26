__author__ = 'ashahab'
import webapp2
from boilerplate.lib.basehandler import BaseHandler
from boilerplate import forms
from src.joinhour.token_generator import TokenGenerator
from webapp2_extras.i18n import gettext as _


class TokenGeneratorHandler(BaseHandler):
    """
    Handles the matching making requests.
    At the end of matchmaking pushes the result to notification queue.
    """
    def get(self):
        """ Returns a simple HTML for contact form """

        if not self.user:
            return self.redirect_to('login')
        params = {
            "exception" : self.request.get('exception')
        }
        return self.render_template('token_generator.html', **params)

    def post(self):
        number_of_tokens = int(self.form.num_tokens.data.strip())
        TokenGenerator.create_tokens(number_of_tokens)
        message = _('Successfully generated tokens.')
        self.add_message(message, 'success')
        self.redirect_to('token_generator')

    @webapp2.cached_property
    def form(self):
        return forms.TokenForm(self)



