__author__ = 'ashahab'
from google.appengine.api import channel

from boilerplate.lib.basehandler import BaseHandler, user_required
from src.joinhour.models.activity import Activity
from src.joinhour.activity_manager import ActivityManager
from boilerplate import models
from src.joinhour.models.user_activity import UserActivity
from src.joinhour.utils import *
from src.joinhour.notification_manager import NotificationManager


class CancelActivityHandler(BaseHandler):
    """
    Handler for JoinHandler Form
    """

    @user_required
    def get(self):
        return self.redirect_to('home')

    @user_required
    def post(self):
        activity_key = self.request.get('activity_key')
        #invoke unjoin for given user and activity
        activity_manager = ActivityManager.get(activity_key)
        success, message = activity_manager.unjoin(self.user_id)
        if success:
            user_info = models.User.get_by_id(long(self.user_id))
            channel.send_message(activity_manager.get_activity().username, "A user has left your activity: " + user_info.username)
            self.add_message(message, 'success')
            self._push_notification(user_info, activity_manager)
        #fire a notification to the activity owner
        else:
            self.add_message(message, 'error')
        return self.redirect_to('home')


    def _push_notification(self,cancelling_user,activity_manager):
        email_url = self.uri_for('taskqueue-send-email')
        activity_owner = models.User.get_by_username(activity_manager.get_activity().username)
        #all users signed up for this activity
        participants_list = UserActivity.query(UserActivity.activity == activity_manager.get_activity().key).fetch(projection = [UserActivity.user])
        participants = [activity_owner.name + ' ' + activity_owner.last_name]
        for participant in participants_list:
            participants.append(str(participant.user.get().name) + ' ' + str(participant.user.get().last_name))


        #To the activity owner
        template_val = {
            "app_name": self.app.config.get('app_name'),
            "owner_name":activity_owner.name+' '+activity_owner.last_name,
            "activity": activity_manager.get_activity(),
            "cancelling_user_name":cancelling_user.name+' '+cancelling_user.last_name,
            "complete": activity_manager.status() == Activity.COMPLETE,
            "expires_in": minute_format(activity_manager.expires_in()),
            "participants":','.join(participants)
        }
        notification_manager = NotificationManager.get()
        notification_manager.push_notification(activity_owner.email,
                                               '[JoinHour.com]Cancellation',
                                               'emails/join_cancel_notification.txt',
                                               **template_val)