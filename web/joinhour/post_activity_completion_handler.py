__author__ = 'aparbane'
from google.appengine.ext import ndb
from src.joinhour.models.feedback import ActivityFeedback



from boilerplate.lib.basehandler import BaseHandler


class PostActivityCompletionHandler(BaseHandler):

    def get(self):
        activity_key = self.request.get('activity_key')
        activity = ndb.Key(urlsafe=activity_key).get()
        #Double check if the activity still exists and still complete
        if activity is not None and activity.status == 'COMPLETE':
            self._handleFeedBack(activity)


    def _handleFeedBack(self,activity):
        activity_feedback = ActivityFeedback()
        activity_feedback.activity = activity
        activity_feedback.put()


