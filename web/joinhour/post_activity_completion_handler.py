from src.joinhour.models.event import Event

__author__ = 'aparbane'
from google.appengine.ext import ndb
from src.joinhour.models.feedback import UserFeedback
from src.joinhour.models.user_activity import UserActivity
from boilerplate import models
import logging

from boilerplate.lib.basehandler import BaseHandler


class PostActivityCompletionHandler(BaseHandler):
    def get(self):
        try:
            activity_key = self.request.get('activity_key')
            activity = ndb.Key(urlsafe=activity_key).get()
            #Double check if the activity still exists and still complete
            if activity is not None and activity.status == Event.FORMED_INITIATED:
                activity.status = Event.COMPLETE_NEEDS_FEEDBACK
                self._handleFeedBack(activity)
        except Exception , e:
            logging.warn(e)


    def _handleFeedBack(self, activity):
        activity_user = models.User.get_by_username(activity.username)
        #all users signed up for this activity
        participants_list = UserActivity.query(UserActivity.activity == activity.key, UserActivity.status == UserActivity.ACTIVE).fetch(
            projection=[UserActivity.user])
        #Ask feedback from participants
        for participant in participants_list:
            user_feedback = UserFeedback()
            user_feedback.activity = activity.key
            user_feedback.user = participant.user
            user_feedback.put()
            #Ask feedback from owner
        user_feedback = UserFeedback()
        user_feedback.activity = activity.key
        user_feedback.user = activity_user.key
        user_feedback.put()

