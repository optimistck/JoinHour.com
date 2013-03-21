from src.joinhour.models.user_activity import UserActivity

__author__ = 'ashahab'
from webapp2_extras.i18n import gettext as _
from google.appengine.ext import ndb
import webapp2
from boilerplate.lib.basehandler import BaseHandler
from boilerplate import forms
from boilerplate import models
from src.joinhour.activity_manager import ActivityManager
from google.appengine.api import taskqueue
from src.joinhour.models.activity import Activity
# import handlers


class JoinActivityHandler(BaseHandler):
    """
    Handler for JoinHandler Form
    """

    #TODO: load the categories and sub-categories from the pull-down menu
    def get(self):
        user_id = self.user_id
        key = self.request.get('key')
        activity_manager = ActivityManager.get(key)
        (success, message) = activity_manager.connect(user_id)
        if success:
            message = _("Congratulations! You joined an activity for " + ndb.Key(urlsafe=key).get().category)
            self._push_notification(user_id,activity_manager)
            self.add_message(message, 'success')
            return self.redirect_to('activity')
        else:
            self.add_message(message, 'failure')
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

    def _push_notification(self,user_id,activity_manager):
        user = models.User.get_by_id(long(user_id))
        email_url = self.uri_for('taskqueue-send-email')
        activity_user = models.User.get_by_username(activity_manager.get_activity().username)
        participants_list = UserActivity.query(UserActivity.activity == activity_manager.get_activity().key).fetch(projection = [UserActivity.user])
        participants = []
        for participant in participants_list:
            participants.append(str(participant.user.get().name) + ' ' + str(participant.user.get().last_name))

        #To the activity owner
        template_val = {
            "app_name": self.app.config.get('app_name'),
            "owner_name":activity_user.name+' '+activity_user.last_name,
            "activity": activity_manager.get_activity(),
            "participant_username":user.name+' '+user.last_name,
            "complete": activity_manager.status() == Activity.COMPLETE,
            "expires_in": activity_manager.expires_in(),
            "participants":','.join(participants)
        }
        body = self.jinja2.render_template('emails/activity_new_companion_notification_for_activity_owner.txt', **template_val)
        taskqueue.add(url = email_url,params={
            'to':activity_user.email,
            'subject' : '[JoinHour.com]New companion for your activity',
            'body' : body
        })

        if activity_manager.status() == Activity.COMPLETE :
            for participant in participants_list:
                template_val = {
                    "app_name": self.app.config.get('app_name'),
                    "owner_name":activity_user.name+' '+activity_user.last_name,
                    "activity": activity_manager.get_activity(),
                    "participant_username":participant.user.get().name+' '+participant.user.get().last_name,
                    "expires_in": activity_manager.expires_in(),
                    "participants":','.join(participants)
                }
                body = self.jinja2.render_template('emails/activity_go_notification_for_activity_participant.txt', **template_val)
                taskqueue.add(url = email_url,params={
                    'to':activity_user.email,
                    'subject' : '[JoinHour.com]Your activity is a GO',
                    'body' : body
                })



