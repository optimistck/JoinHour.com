__author__ = 'ashahab'

from boilerplate.lib.basehandler import BaseHandler
from src.joinhour.models.user_activity import UserActivity
from boilerplate import models
from google.appengine.api import taskqueue
from urlparse import urlparse
from google.appengine.ext import ndb
from webapp2_extras.appengine.auth.models import User
from src.joinhour.activity_manager import ActivityManager
from google.appengine.api import taskqueue
from src.joinhour.models.activity import Activity
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
                    users_for_activity = UserActivity.get_users_for_activity(activity)
                    self._process_notification(users_for_activity)
        except Exception , e:
            print e

    def _process_notification(self,users_for_activity):
        participants = []
        for userActivity in users_for_activity:
            participants.append(userActivity.user.name+' '+userActivity.user.last_name)
        for userActivity in users_for_activity:
            self._notify_interest_owner(userActivity, participants)

    def _notify_interest_owner(self,userActivity, participants):
        user = userActivity.user
        activity = userActivity.activity
        activity_owner = User.get_by_username(activity.username)
        email_url = self.uri_for('taskqueue-send-email')
        url_object = urlparse(self.request.url)

        template_val = {
            "app_name": self.app.config.get('app_name'),
            "participant_username": user.name+' '+user.last_name,
            "activity_category": activity.category,
            "owner_name": activity_owner.name+' '+activity_owner.last_name,
            "expires_in": ActivityManager.get(activity.key.urlsafe()).expires_in(),
            "participants":participants,
            "support_url" : url_object.scheme + '://' + str(url_object.hostname) + ':' +str(url_object.port)
        }
        body = self.jinja2.render_template('emails/its_a_go_notification_for_participants.txt', **template_val)
        taskqueue.add(url = email_url,params={
            'to': user.email,
            'subject' : '[JoinHour.com]Its a go!',
            'body' : body
        })




