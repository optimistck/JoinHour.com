__author__ = 'aparbane'

from  datetime import datetime
from datetime import timedelta
import os

from google.appengine.ext import ndb
from google.appengine.api.taskqueue import Task

from src.joinhour.models.activity import Activity
from src.joinhour.models.match import Match
from src.joinhour.models.interest import Interest
from src.joinhour.models.user_activity import UserActivity
from src.joinhour.interest_manager import InterestManager
from boilerplate import models


class ActivityManager(object):


    @classmethod
    def create_activity(cls,**kwargs):
        '''
        Creates a new activity with the arguments specified.
        After creation Starts initiates the matchmaker task for finding a possible match and also initiates the activity lifecycle task
        :param cls:
        :param kwargs:
        :return: The newly created activity
        '''
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
            expiration_time = int(str(activity.expiration))
            timezone_offset = datetime.now() - datetime.utcnow()
            task_execution_time = activity.date_entered + timedelta(minutes=expiration_time) - timedelta(minutes=5) + timezone_offset
            goTask = Task(eta=task_execution_time, url='/activity_life_cycle/',method='GET',params={'activity': activity.key.urlsafe()})
            goTask.add('activityLifeCycle')
        return activity

    @classmethod
    def create_activity_from_interest(cls, **kwargs):
        '''
        Creates a new activity from an interest. Also joins the interest owner with the activity. The interest is marked as COMPLETE and the match table is populated.
        :param cls:
        :param kwargs:
        :return:
        '''
        interest = ndb.Key(urlsafe=kwargs['interest_id']).get()
        if InterestManager.get(interest.key.urlsafe()).expires_in() == Interest.EXPIRED:
            return False, "Cannot create activity from expired interest"
        #Create the activity
        activity = ActivityManager.create_activity(
                                        building_name=interest.building_name,category=interest.category,
                                        duration=interest.duration,expiration = interest.expiration,
                                        username = kwargs['username'],note = kwargs['note'],
                                        ip = kwargs['ip'],
                                        min_number_of_people_to_join = kwargs['min_number_of_people_to_join'],
                                        max_number_of_people_to_join = kwargs['max_number_of_people_to_join'])
        #mark interest complete
        interest.status = interest.COMPLETE
        user = models.User.get_by_username(interest.username)
        success, message = ActivityManager.get(activity.key.urlsafe()).connect(user.key.id())
        interest.put()
        #mark this as match found
        match = Match(interest=interest.key,
                      activity=activity.key)
        match.put()
        #Notify interest owner
        return success, message, user.key.id(), activity.key.urlsafe()

    @classmethod
    def get(cls,key):
        '''
        Returns a Handle to the activity manager for an activity key
        :param cls:
        :param key: ActivityKey
        :return:
        '''
        return ActivityManager(key)

    def __init__(self,key):
        self._activity = ndb.Key(urlsafe=key).get()

    def connect(self,user_id):
        '''
        Connects/Joins an user with provided user_id with the activity for the current activity manager
        :param user_id:
        :return:
        '''
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
        self._activity.status = new_status
        self._activity.put()
