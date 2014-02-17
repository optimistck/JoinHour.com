__author__ = 'apbanerjee'


from boilerplate import models


from boilerplate.lib.basehandler import BaseHandler, user_required

from src.joinhour.notification_manager import NotificationManager
from src.joinhour.models.notification import Notification

from src.joinhour.request_manager import RequestManager
from src.joinhour.event_manager import EventManager
from src.joinhour.utils import *


class JoinRequestHandler(BaseHandler):

    @user_required
    def get(self):
        action = self.request.get('action')
        request_key = self.request.get('request_key')
        request_manager = RequestManager.get(request_key)
        activity_manager = EventManager.get(request_manager.get_request().activity.urlsafe())
        if action == "Accept":
            (success, message) = request_manager.accept()
            if success:
                self.add_message(message, 'success')
                self._push_notification(activity_manager)
            else:
                self.add_message(message, 'failure')
        elif action == "Reject":
            request_manager.reject()
        elif action == "Cancel":
            request_manager.cancel()
        return self.redirect_to('pipeline')

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





