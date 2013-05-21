import logging
import webapp2
from boilerplate import models
from boilerplate.lib.basehandler import BaseHandler, user_required
from web.joinhour.ui import forms

__author__ = 'aparup'

class CompleteProfileSocialUserHandler(BaseHandler):

    @user_required
    def get(self):
        logging.info('Get : CompleteProfileSocialUserHandler')
        return self.render_template('complete_profile_social_user.html')

    @user_required
    def post(self):
        logging.info('Post : CompleteProfileSocialUserHandler')
        building = self.form.building.data
        user_info = models.User.get_by_id(long(self.user_id))
        user_info.building = building
        user_info.put()
        self.redirect_to('home')

    @webapp2.cached_property
    def form(self):
        return forms.CompleteProfileForSocialUserForm(self)


