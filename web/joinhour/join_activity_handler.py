from google.appengine.api import taskqueue

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
        (success, message) = activity_manager.connect(user_id)
        if success:
            message = _("Congratulations! You joined an activity for " + activity_id)
            self._push_notification(user_id,activity_manager.get_activity())
        self.add_message(message, 'success')
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

    def _push_notification(self,user_id,activity):

        user = models.User.get_by_id(long(user_id))
        activity_user = models.User.get_by_username(activity.username)
        template_val = {
            "app_name": self.app.config.get('app_name'),
            "activity_creator_username": activity.username,
            "activity_category": activity.category,
            "activity_note": activity.note,
            "requester_name":user.username,
            "requester_building":user.building,
            "requester_email":user.email,
        }
        email_url = self.uri_for('taskqueue-send-email')
        body = self.jinja2.render_template('emails/join_request_notification.txt', **template_val)
        taskqueue.add(url = email_url,params={
            'to':activity_user.email,
            'subject' : '[JoinHour.com]Connect request',
            'body' : body
        })


