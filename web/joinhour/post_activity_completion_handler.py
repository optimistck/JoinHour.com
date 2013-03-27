from google.appengine.ext import ndb
from boilerplate import models
from src.joinhour.models.user_activity import UserActivity

__author__ = 'aparbane'

from boilerplate.lib.basehandler import BaseHandler


class PostActivityCompletionHandler(BaseHandler):

    def get(self):
        activity_key = self.request.get('activity_key')
        activity = ndb.Key(urlsafe=activity_key).get()
        #Double check if the activity still exists and still complete
        if activity is not None and activity.status == 'COMPLETE':
            #find all users for this activity
            activity_owner = models.User.get_by_username(activity.username)
            users = [activity_owner]
            for user_activity in UserActivity.query(UserActivity.activity == activity.key):
                users.append(user_activity.user.get())
            self.handleFeedBack(activity,users)

    def handleFeedBack(self,activity,users=[]):
        #Hookup the feedback management code here
        pass


