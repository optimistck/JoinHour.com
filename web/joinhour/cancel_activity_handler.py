__author__ = 'ashahab'
from google.appengine.api import channel
from boilerplate.lib.basehandler import BaseHandler, user_required
from src.joinhour.event_manager import EventManager
from boilerplate import models
from src.joinhour.models.event import Event
from src.joinhour.utils import *
from src.joinhour.notification_manager import NotificationManager
from google.appengine.ext import ndb

class CancelActivityHandler(BaseHandler):
    """
    Handler for Cancelling an interest by the interest owner
    """

    @user_required
    def get(self):
        return self.post()

    @user_required
    def post(self):
        event_manager = EventManager.get(self.request.get('activity_key'))
        #invoke unjoin for given user and activity
        participants = event_manager.get_all_companions()
        category = event_manager.get_event().category
        activity_username = event_manager.get_event().username
        success, message = event_manager.cancel()
        if success:
            activity_user = models.User.get_by_username(activity_username)
            activity_owner_name = activity_user.name + ' ' + activity_user.last_name
            for participant in participants:
                participant_user = participant.user.get()
                channel.send_message(participant_user.name, "Your activity has been canceled by: " + activity_owner_name)
                self._push_notification(category,activity_owner_name,participant_user,'No reason')
            self.add_message(message, 'success')
        else:
            self.add_message(message, 'error')
        #fire a notification to the activity owner
        return self.redirect_to('pipeline')


    def _push_notification(self,category,activity_owner_name,participant,reason_for_cancellation):

        template_val = {
            "app_name": self.app.config.get('app_name'),
            "activity_name": category,
            "activity_owner_name": activity_owner_name,
            "participant_username": participant.name+' '+participant.last_name,
            "reason_for_cancellation":reason_for_cancellation
        }
        notification_manager = NotificationManager.get()
        notification_manager.push_notification(participant.email,
                                               '[JoinHour.com]Activity cancellation notification',
                                               'emails/activity_cancel_notification_for_participant.txt',
                                               **template_val)