from webapp2_extras.i18n import gettext as _
from google.appengine.ext import ndb
from models.Activity import Activity 
import webapp2
from boilerplate.lib.basehandler import BaseHandler 
from boilerplate import forms
from boilerplate import models



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
        building_name = 'building_name'

        if self.user:
            user_info = models.User.get_by_id(long(self.user_id))        
            activitity = Activity(parent=ndb.Key("ActivityKey", building_name),
                            category = self.form.category.data.strip(),
                            min_number_of_people_to_join = self.form.min_number_of_people_to_join.data.strip(),
                            max_number_of_people_to_join = self.form.max_number_of_people_to_join.data.strip(),
                            duration = self.form.duration.data.strip(),
                            expiration = self.form.expiration.data.strip(),
                            note = self.form.note.data.strip(),
                            username = user_info.username,
                            ip = self.request.remote_addr
                            )
            activitity.put()

            message = _("Your interest was registered successfully. We are searching for a match ... ")
            self.add_message(message, 'success')
            return self.redirect_to('activity')

    @webapp2.cached_property
    def form(self):
        return forms.JoinForm(self)