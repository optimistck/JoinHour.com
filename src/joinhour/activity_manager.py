__author__ = 'aparbane'

from src.joinhour.models.activity import Activity
from src.joinhour.models.user_activity import UserActivity
from boilerplate import models
from google.appengine.ext import ndb
from  datetime import datetime
from datetime import timedelta
from google.appengine.api.taskqueue import Task
import os


class ActivityManager(object):

    '''
    TODO- Following a stateful model for this as of now. Do we need a more stateless implementation of activity manager in future?
    Things to think about
    * Concurrency
    * Memory
    '''

    @classmethod
    def create_activity(cls,**kwargs):
        activity = Activity(category = kwargs['category'],
                            duration = kwargs['duration'],
                            expiration = kwargs['expiration'],
                            note = kwargs['note'],
                            ip = kwargs['ip'],
                            min_number_of_people_to_join = kwargs['min_number_of_people_to_join'],
                            max_number_of_people_to_join = kwargs['max_number_of_people_to_join'],
                            username = kwargs['username'],
                            building_name = kwargs['building_name'],
                            date_entered = datetime.utcnow()
        )
        activity.put()
        if os.environ.get('ENV_TYPE') is None:
            task = Task(url='/match_maker/',method='GET',params={'activity': activity.key.urlsafe()})
            task.add('matchmaker')
        return activity

    @classmethod
    def get(cls,key):
        return ActivityManager(key)

    def __init__(self,key):
        self._activity = ndb.Key(urlsafe=key).get()

    def connect(self,user_id,**kwargs):
        (canJoin, message) = self.can_join(user_id)
        if not canJoin:
            return False, message

        #Need to validate whether the same user has signed up for the same activity
        user_info = models.User.get_by_id(long(user_id))
        user_activity = UserActivity(user=user_info.key,
                                     activity=self._activity.key)
        user_activity.put()
        self._activity.headcount += 1
        #An activity will be marked as COMPLETE if it satisfies the minm number of people required requirement
        if self._activity.status == Activity.INITIATED or self._activity.status == Activity.FORMING:
            if self._is_complete():
                self._change_status(Activity.COMPLETE)
            else:
                self._change_status(Activity.FORMING)
        return True, message

    def spots_remaining(self):
        max_count = int(self._activity.max_number_of_people_to_join.split()[0])
        return max_count - self._activity.headcount

    def _is_complete(self):
        min_count = int(self._activity.min_number_of_people_to_join.split()[0])
        return min_count <= self._activity.headcount




    def mark_expired(self):
        self._change_status(Activity.EXPIRED)

    def can_join(self, userId):
        #First check the status
        if self.expires_in() == Activity.EXPIRED:
            return False, "Activity is already expired"
        #Are there any activities with this user and this activity?
        user_info = models.User.get_by_id(long(userId))
        if self._activity.username == user_info.username:
            return False, "You yourself created this activity."
        user_activity = UserActivity.get_by_user_activity(user_info.key, self._activity.key)
        if user_activity:
            return False, "You have already joined this activity."
        #Now check if there are spots remaining
        elif self._activity.max_number_of_people_to_join == 'No Limit':
            return True, "Success"
        else:
            headcount = self._activity.headcount
            max_count = int(self._activity.max_number_of_people_to_join.split()[0])
            if headcount < max_count:
                return True, "Success"
            return False, "This activity is full."

    def status(self):
        return self._activity.status

    def get_activity(self):
        return self._activity

    def expires_in(self):
        if self._activity.status == Activity.EXPIRED:
            return Activity.EXPIRED
        else:
            expiration_time = int(str(self._activity.expiration))
            now = datetime.utcnow()
            activity_creation_date = self._activity.date_entered
            if now < (activity_creation_date + timedelta(minutes=expiration_time)):
                return  (activity_creation_date + timedelta(minutes=expiration_time)) - now
            return Activity.EXPIRED

    def _change_status(self,new_status):
        #TODO Need to think about Thread safety here
        #TODO Once the activity is expired or complete need to move it to a different table. Primarly for analytics support
        self._activity.status = new_status
        self._activity.put()








