__author__ = 'aparbane'

from src.joinhour.models.activity import Activity
from src.joinhour.models.user_activity import UserActivity
from boilerplate import models
from google.appengine.ext import ndb
from  datetime import datetime
from datetime import timedelta




class ActivityManager(object):

    '''
    TODO- Following a stateful model for this as of now. Do we need a more stateless implementation of activity manager in future?
    Things to think about
    * Concurrency
    * Memory
    '''

    @classmethod
    def create_activity(cls,**kwargs):
        activity = Activity(parent=ndb.Key("ActivityKey", kwargs['building_name']),
                            category = kwargs['category'],
                            duration = kwargs['duration'],
                            expiration = kwargs['expiration'],
                            note = kwargs['note'],
                            ip = kwargs['ip'],
                            min_number_of_people_to_join = kwargs['min_number_of_people_to_join'],
                            max_number_of_people_to_join = kwargs['max_number_of_people_to_join'],
                            username = kwargs['username']
        )
        activity.put()

    @classmethod
    def get(cls,activityId):
        return ActivityManager(activityId)

    def __init__(self,activity_id):
        self._activity = Activity.get_by_id(long(activity_id),parent=ndb.Key("ActivityKey", 'building_name'))

    def connect(self,user_id,**kwargs):
        (canJoin, message) = self.can_join(user_id)
        if not canJoin:
            return False, message

        #Need to validate whether the same user has signed up for the same activity
        user_info = models.User.get_by_id(long(user_id))
        user_activity = UserActivity(parent=ndb.Key("UserActivityKey", user_info.username),
                                     user=user_info.key,
                                     activity=self._activity.key)
        user_activity.put()
        #If the status is INITIATED change it to FORMING
        self._activity.headcount += 1
        if self._activity.status == Activity.INITIATED and self.can_start():
            self._change_status(Activity.FORMING)
            #else If the status is FORMING
            #If this would be the last spot change status to COMPLETE
            #Queue a task in JoinNotificationQueue for notifying user
        if self.spots_remaining() == 0:
            self._change_status(Activity.COMPLETE)
            #else Don't change the status
            #Queue a task in JoinNotificationQueue for notifying user
        return True, message

    def spots_remaining(self):
        max_count = int(self._activity.max_number_of_people_to_join.split()[0])
        return max_count - self._activity.headcount

    def can_start(self):
        min_count = int(self._activity.min_number_of_people_to_join.split()[0])
        return min_count <= self._activity.headcount

    def mark_expired(self):
        self._change_status(Activity.EXPIRED)

    def can_join(self, userId):
        #First check the status
        if self._activity == Activity.EXPIRED or self._activity == Activity.COMPLETE:
            return False, "Activity is expired or complete."
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
            max_count = self._activity.max_number_of_people_to_join.split()[0]
            if headcount < max_count:
                return True, "Success"
            return False, "This activity is full."

    def status(self):
        return self._activity.status

    def expires_in(self):
        if self._activity.status == Activity.EXPIRED:
            return Activity.EXPIRED
        else:
            expiration_time = int(str(self._activity.expiration))
            now = datetime.now()
            if now < (self._activity.date_entered + timedelta(minutes=expiration_time)):
                return  (self._activity.date_entered + timedelta(minutes=expiration_time)) - now
            return Activity.EXPIRED

    def _change_status(self,new_status):
        #TODO Need to think about Thread safety here
        #TODO Once the activity is expired or complete need to move it to a different table. Primarly for analytics support
        self._activity.status = new_status
        self._activity.put()


