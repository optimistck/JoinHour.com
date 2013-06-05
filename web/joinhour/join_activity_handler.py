from src.joinhour.models.notification import Notification

__author__ = 'ashahab'
from webapp2_extras.i18n import gettext as _
import webapp2
from google.appengine.api import channel

from boilerplate.lib.basehandler import BaseHandler, user_required
from boilerplate import forms
from boilerplate import models
from src.joinhour.event_manager import EventManager
from src.joinhour.utils import *
from src.joinhour.notification_manager import NotificationManager
from src.joinhour.models.user_activity import UserActivity


class JoinActivityHandler(BaseHandler):
    """
    Handler for JoinHandler Form
    """

    @user_required
    def get(self):
        user_id = self.user_id
        key = self.request.get('key')
        activity_manager = EventManager.get(key)
        (success, message) = activity_manager.connect(user_id)
        if success:
            activity = activity_manager.get_event()
            message = _("Congratulations! You joined an activity for " + activity.category)
            user_info = models.User.get_by_id(long(user_id))
            channel.send_message(activity.username, "a user has joined your activity: " + user_info.username)
            self._push_notification(user_id, activity_manager)
            self.add_message(message, 'success')
            return self.redirect_to('activity')
        else:
            self.add_message(message, 'failure')
            return self.redirect_to('activity')

    def post(self):
        return self.redirect_to('activity')

    @webapp2.cached_property
    def form(self):
        return forms.JoinActivityForm(self)

    def _push_notification(self, user_id, activity_manager):
        user = models.User.get_by_id(long(user_id))
        activity_user = models.User.get_by_username(activity_manager.get_event().username)
        #all users signed up for this activity
        participants_list = UserActivity.query(UserActivity.activity == activity_manager.get_event().key,UserActivity.status == UserActivity.ACTIVE).fetch(
            projection=[UserActivity.user])
        participants = [activity_user.name + ' ' + activity_user.last_name]
        for participant in participants_list:
            participants.append(str(participant.user.get().name) + ' ' + str(participant.user.get().last_name))
        #To the activity owner
        if activity_manager.status() in [Event.FORMED_OPEN, Event.FORMED_INITIATED]:
            template_val = {
                "app_name": self.app.config.get('app_name'),
                "owner_name": activity_user.name + ' ' + activity_user.last_name,
                "activity": activity_manager.get_event(),
                "participant_username": user.name + ' ' + user.last_name,
                "complete": activity_manager.status() == Event.COMPLETE,
                "expires_in": minute_format(activity_manager.expires_in()),
                "participants": ','.join(participants)
            }
            notification_manager = NotificationManager.get(self)
            notification_manager.push_notification2(activity_user.email,
                                               '[JoinHour.com]Activity Go Notification',
                                               'emails/activity_go_notification_for_activity_participant.txt',Notification.GO_NOTIFICATION,
                                               activity_manager.get_event(),activity_user,True,**template_val)

        #To the activity participants in case the activity is a GO
        if activity_manager.status() in [Event.FORMED_OPEN, Event.FORMED_INITIATED]:
            for participant in participants_list:
                template_val = {
                    "app_name": self.app.config.get('app_name'),
                    "owner_name": activity_user.name + ' ' + activity_user.last_name,
                    "activity": activity_manager.get_event(),
                    "participant_username": participant.user.get().name + ' ' + participant.user.get().last_name,
                    "expires_in": minute_format(activity_manager.expires_in()),
                    "participants": ','.join(participants)
                }
                notification_manager.push_notification2(participant.user.get().email,
                                                       '[JoinHour.com]Activity Go Notification',
                                                       'emails/activity_go_notification_for_activity_participant.txt',Notification.GO_NOTIFICATION,activity_manager.get_event(),participant.user.get(),True,
                                                       **template_val)








