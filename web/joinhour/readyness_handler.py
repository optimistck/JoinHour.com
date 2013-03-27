__author__ = 'ashahab'

from boilerplate.lib.basehandler import BaseHandler
from src.joinhour.models.user_activity import UserActivity
from boilerplate import models
from google.appengine.api import taskqueue
from urlparse import urlparse
from google.appengine.ext import ndb
from webapp2_extras.appengine.auth.models import User
from src.joinhour.activity_manager import ActivityManager
from UserString import MutableString
from src.joinhour.models.activity import Activity
from boilerplate.models import User
class ReadynessHandler(BaseHandler):
    """
    Handles the matching making requests.
    At the end of matchmaking pushes the result to notification queue.
    """
    def get(self):
        try:
            activity_key = self.request.get('activity')

            if activity_key != '':
                activity = ndb.Key(urlsafe=activity_key).get()
                if activity.status == Activity.COMPLETE:

                    userActivities = UserActivity.get_users_for_activity(activity.key)
                    participants = self._process_notification(userActivities)
                    activity_owner = User.get_by_username(activity.username)
                    self._notify_participants(activity_owner, activity, participants)
        except Exception , e:
            print e

    def _process_notification(self,users_for_activity):
        participants = MutableString()
        for userActivity in users_for_activity:
            user = userActivity.user.get()
            participants += str(user.name)+' ' + str(user.last_name) + ' , '
            participants.rstrip(',')

        for userActivity in users_for_activity:
            user = userActivity.user.get()
            activity = userActivity.activity.get()
            self._notify_participants(user, activity, participants)
        return participants

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
        body = self.jinja2.render_template('emails/its_a_go_notification_for_participants.txt', **template_val)
        taskqueue.add(url = email_url,params={
            'to': user.email,
            'subject' : '[JoinHour.com]Its a go!',
            'body' : body
        })




