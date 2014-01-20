__author__ = 'aparup'

import logging
import webapp2
from boilerplate import models
from boilerplate.lib.basehandler import BaseHandler, user_required
from web.joinhour.ui import forms
from src.joinhour.models.token import Token
from webapp2_extras.i18n import gettext as _
class CompleteProfileSocialUserHandler(BaseHandler):




    @user_required
    def get(self):
        logging.info('Get : CompleteProfileSocialUserHandler')
        return self.render_template('complete_profile_social_user.html')

    @user_required
    def post(self):
        logging.info('Post : CompleteProfileSocialUserHandler')

        building = "TEMP"
        security_code = self.form.security_code.data.strip();
        if security_code:
            try:
                token_match = Token.match(security_code)
                building = token_match.belongs_to_group
            except ValueError:
                token_match = None
            if not token_match or token_match.used:
                message = _('Sorry, invalid security code. Please try again or request a new code from the group organizer.')
                self.add_message(message, 'error')
                return self.redirect_to('complete_profile_social_user')
            else:
                token_match.used = True
                token_match.put();
        user_info = models.User.get_by_id(long(self.user_id))
        user_info.building = building
        user_info.put()
        self.redirect_to('home')

    @webapp2.cached_property
    def form(self):
        return forms.CompleteProfileForSocialUserForm(self)


