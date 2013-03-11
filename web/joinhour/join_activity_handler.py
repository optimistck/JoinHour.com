__author__ = 'ashahab'
from webapp2_extras.i18n import gettext as _
from google.appengine.ext import ndb
import webapp2
from boilerplate.lib.basehandler import BaseHandler
from boilerplate import forms
from boilerplate import models
from src.joinhour.activity_manager import ActivityManager
from src.joinhour.models.activity import Activity
# import handlers


class JoinActivityHandler(BaseHandler):
    """
    Handler for JoinHandler Form
    """

    #TODO: load the categories and sub-categories from the pull-down menu
    def get(self):
        user_id = self.user_id
        activity_id = self.request.get('activity_id')
        activity_manager = ActivityManager.get(activity_id)
        activity_manager.connect(user_id)

        return self.redirect_to('activity')

    def post(self):
        # if not self.form.validate():
        #     return self.get()
        # if not self.user:
        #     return handlers.LoginHandler.get(self)
        # #TODO: the building name needs to come from the user profile
        user_id = self.user_id
        # activity_id = self.form.activity_id
        # message = _("Congratulations! You joined an activity for " + activity_id)
        # self.add_message(message, 'success')
        return self.redirect_to('activity')

    @webapp2.cached_property
    def form(self):
        return forms.JoinActivityForm(self)

