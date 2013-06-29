import os
from google.appengine.api.taskqueue import Task
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
            #Launch the feedback process
            if activity is not None and activity.status == Event.FORMED_INITIATED:
                activity.status = Event.COMPLETE_NEEDS_FEEDBACK
                activity.put()
                self._handleFeedBack(activity)
                self._start_activity_closure_process(activity)
            #Close the activity
            elif activity is not None and activity.status == Event.COMPLETE_NEEDS_FEEDBACK:
                activity.status = Event.CLOSED
                activity.put()
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


    def _start_activity_closure_process(self, activity):
        if os.environ.get('ENV_TYPE') is None:
            if os.environ.get('SERVER_SOFTWARE', '').startswith('Development'):
                eta = 1800
            else:
                eta = 259200
            task = Task(url='/activity_closure/', method='GET',
                        params={'activity_key': activity.key.urlsafe()},
                        countdown=eta)
            task.add('activityClosure')

