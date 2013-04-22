__author__ = 'ashahab'

from urlparse import urlparse
from UserString import MutableString
from  datetime import datetime
from datetime import timedelta
import os
import logging
from google.appengine.ext import ndb
from google.appengine.api.taskqueue import Task
from boilerplate.lib.basehandler import BaseHandler
from src.joinhour.models.user_activity import UserActivity
from boilerplate import models
from src.joinhour.activity_manager import ActivityManager
from src.joinhour.models.activity import Activity
from src.joinhour.notification_manager import NotificationManager

class ActivityLifeCycleHandler(BaseHandler):

    def get(self):
        try:
            activity_key = self.request.get('activity')
            if activity_key != '':
                activity = ndb.Key(urlsafe=activity_key).get()
                if not activity:
                    return
                if activity.status == Activity.COMPLETE:
                    self._start_post_activity_completion_process(activity)
                    self._send_readyness_notification(activity)

        except Exception , e:
            logging.warn(e)

    def _send_readyness_notification(self,activity):
        userActivities = UserActivity.get_users_for_activity(activity.key)
        participants = MutableString()
        for userActivity in userActivities:
            user = userActivity.user.get()
            participants += str(user.name)+' ' + str(user.last_name) + ' , '
            participants.rstrip(',')
        activity_owner = models.User.get_by_username(activity.username)
        self._notify_participants(activity_owner, activity, participants)

    def _start_post_activity_completion_process(self,activity):
        if os.environ.get('ENV_TYPE') is None:
            #Calculate the eta
            expiration_time = int(str(activity.expiration))
            if os.environ.get('SERVER_SOFTWARE','').startswith('Development'):
                eta = 120
            else :
                eta = int(activity.duration) * 60
                activity_start_time = activity.date_entered + timedelta(minutes=expiration_time)
                now = datetime.utcnow()
                if now < activity_start_time:
                    eta = eta + (activity_start_time - now).total_seconds()
            task = Task(url='/post_activity_completion/',method='GET',
                        params={'activity_key': activity.key.urlsafe()},
                        countdown=eta)
            task.add('postActivityCompletion')


    def _notify_participants(self,user, activity, participants):
        activity_owner = models.User.get_by_username(activity.username)
        email_url = self.uri_for('taskqueue-send-email')
        url_object = urlparse(self.request.url)

        template_val = {
            "app_name": self.app.config.get('app_name'),
            "participant_username": user.name+' '+user.last_name,
            "activity_category": activity.category,
            "owner_name": activity_owner.name+' '+activity_owner.last_name,
            "expires_in": ActivityManager.get(activity.key.urlsafe()).expires_in(),
            "participants": participants,
            "support_url" : url_object.scheme + '://' + str(url_object.hostname) + ':' +str(url_object.port)
        }
        notification_manager = NotificationManager.get(self)
        notification_manager.push_notification(user.email,
                                               '[JoinHour.com]Its a go!',
                                               'emails/its_a_go_notification_for_participants.txt',
                                               **template_val)






