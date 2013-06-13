__author__ = 'ashahab'
from src.joinhour.models.notification import Notification
from webapp2_extras.i18n import gettext as _
import webapp2
from google.appengine.api import channel

from boilerplate.lib.basehandler import BaseHandler, user_required
from boilerplate import forms
from boilerplate import models
from src.joinhour.event_manager import EventManager
from src.joinhour.utils import *
from src.joinhour.notification_manager import NotificationManager


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
            message = _("Congratulations! You joined an activity for " + activity_manager.get_event().category)
            self._push_notification(activity_manager)
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

    def _push_notification(self, activity_manager):
        notification_manager = NotificationManager.get(self)
        activity_user = models.User.get_by_username(activity_manager.get_event().username)
        interest_details = get_interest_details(activity_manager.get_event().key.urlsafe())
         #To the activity owner if the activity is GO (formed OPEN)
        if activity_manager.status()  == Event.FORMED_OPEN:
            template_val = notification_manager.get_base_template()
            template_val['interest'] = interest_details
            notification_manager.push_notification2(activity_user.email,
                                               '[JoinHour.com]Activity Go Notification',
                                               'emails/activity_formed_and_open_for_owner.txt',Notification.GO_NOTIFICATION,
                                               activity_manager.get_event(),activity_user,True,**template_val)

        #To the activity participants in case the activity is a GO (formed OPEN)
        if activity_manager.status() == Event.FORMED_OPEN:
            for participant in activity_manager.get_all_companions():
                template_val = notification_manager.get_base_template()
                template_val['interest'] = interest_details
                template_val['participant_username'] = participant.user.get().username
                notification_manager.push_notification2(participant.user.get().email,
                                                       '[JoinHour.com]Activity Go Notification',
                                                       'emails/activity_formed_and_open_for_participant.txt',Notification.GO_NOTIFICATION,activity_manager.get_event(),participant.user.get(),True,
                                                       **template_val)








