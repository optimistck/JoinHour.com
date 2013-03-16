from webapp2_extras.i18n import gettext as _
from google.appengine.ext import ndb
import webapp2
from boilerplate.lib.basehandler import BaseHandler 
from boilerplate import forms
from boilerplate import models
from src.joinhour.models.activity import Activity
from src.joinhour.interest_manager import InterestManager
from src.joinhour.activity_manager import ActivityManager


class JoinHandler(BaseHandler):
    """
    Handler for JoinHandler Form
    """

    #TODO: load the categories and sub-categories from the pull-down menu
    def get(self):
        params = {}
        return self.render_template('join.html', **params)

    def post(self):
        #TODO: the building name needs to come from the user profile


        if self.user:
            is_create_activity = self.request.get('type_radio') == 'activity'
            user_info = models.User.get_by_id(long(self.user_id))
            building_name = user_info.building
            if is_create_activity:
                ActivityManager.create_activity(building_name=building_name,category=self.form.category.data.strip(),duration=self.form.duration.data.strip(),expiration = self.form.expiration.data.strip(),
                                                username = user_info.username,note = self.form.note.data.strip(),ip = self.request.remote_addr,
                                                min_number_of_people_to_join = self.form.min_number_of_people_to_join.data.strip(),
                                                max_number_of_people_to_join = self.form.max_number_of_people_to_join.data.strip())
            else:
                InterestManager.create_interest(building_name=building_name,category=self.form.category.data.strip(),duration=self.form.duration.data.strip(),expiration = self.form.expiration.data.strip(),
                                                username = user_info.username)
            message = _("Your interest was registered successfully. We are searching for a match ... ")
            self.add_message(message, 'success')
            return self.redirect_to('home')

    @webapp2.cached_property
    def form(self):
        return forms.JoinForm(self)



