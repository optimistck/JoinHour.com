__author__ = 'aparbane'

from  datetime import datetime
from datetime import timedelta
import os

from google.appengine.ext import ndb
from google.appengine.api.taskqueue import Task

from src.joinhour.models.event import Event
from src.joinhour.models.user_activity import UserActivity
from boilerplate import models
import logging


class EventManager(object):


    @classmethod
    def create(cls,**kwargs):
        '''
        Creates an Interest based on the arguments passed in kwargs
        Once an interest is created is added to matchmaker queue
        :param cls:
        :param kwargs:
        :return:
        '''

        event = Event(category = kwargs['category'],
                            date_entered = datetime.utcnow(),
                            type = Event.EVENT_TYPE_FLEX_INTEREST,
                            username = kwargs['username'],
                            building_name = kwargs['building_name'],
        )

        if 'expiration' in kwargs and kwargs['expiration'] != "":
            event.expiration = kwargs['expiration']
        if 'start_time' in kwargs and kwargs['start_time'] != "":
            event.start_time = kwargs['start_time']
        if 'duration' in kwargs and kwargs['duration'] != "":
            event.duration = kwargs['duration']
        if 'min_number_of_people_to_join' in kwargs and kwargs['min_number_of_people_to_join'] != "":
            event.min_number_of_people_to_join = kwargs['min_number_of_people_to_join']
            event.type = Event.EVENT_TYPE_SPECIFIC_INTEREST
        if 'max_number_of_people_to_join' in  kwargs and kwargs['max_number_of_people_to_join'] != "":
            event.max_number_of_people_to_join = kwargs['max_number_of_people_to_join']
        if 'note' in kwargs and kwargs['note'] != "":
            event.note = kwargs['note']
        if 'meeting_place' in kwargs and kwargs['meeting_place'] != "":
            event.meeting_place = kwargs['meeting_place']
        if 'activity_location' in kwargs and kwargs['activity_location'] != "":
            event.meeting_place = kwargs['activity_location']
        event.put()
        if os.environ.get('ENV_TYPE') is None:
            task = Task(url='/match_maker/',method='GET',params={'interest': event.key.urlsafe()})
            task.add('matchmaker')
            logging.info('event created')
            logging.info('match maker task queued')
        return event

    @classmethod
    def get(cls,key):
        '''
        Returns a Handle to the event manager for an event
        :param cls:
        :param key: ActivityKey
        :return:
        '''
        return EventManager(key)

    def __init__(self,key):
        self._event = ndb.Key(urlsafe=key).get()


    def can_leave(self,user_id=None):
        if self.expires_in() == Event.EXPIRED or self._event.status in Event.NON_EDITABLE_STATUS_CHOICES:
            return False, "You cannot leave an expired/closed/initiated/cancelled interest."
        if user_id is not None:
            user = models.User.get_by_id(long(user_id))
            count = UserActivity.query(UserActivity.activity == self._event.key, UserActivity.user == user.key,
                                       UserActivity.status == UserActivity.ACTIVE).count()
            if count == 0:
                return False,"This is not your activity"
        if self._event.status == Event.FORMED_OPEN:
            #TODO Needs some work here to figure out till what time an event can be cancelled
            if self._event.expiration is not None:
                expiration_time = int(str(self._event.expiration))
                now = datetime.now()
                timezone_offset = now - datetime.utcnow()
                last_cancellation_time = self._event.date_entered + timedelta(minutes=expiration_time) - timedelta(minutes=5) + timezone_offset
                if now > last_cancellation_time:
                    return False, "You cannot leave 5 minutes before activity starts."
        return True, "You can leave."

    def unjoin(self, user_id):
        (canLeave, message) = self.can_leave()
        if not canLeave:
            return False, message
        user_info = models.User.get_by_id(long(user_id))
        companion_count = self.companion_count() - 1
        user_activity = UserActivity.get_by_user_activity(user_info.key, self._event.key)
        user_activity.status = UserActivity.CANCELLED
        user_activity.put()
        if not self._can_complete(companion_count):
            self._event.status = Event.FORMING
            self._event.put()
        return True, "user " + user_info.username + " has been successfully removed from activity " + self._event.category

    def cancel(self):
        user_activities = UserActivity.query(UserActivity.activity == self._event.key, UserActivity.status == UserActivity.ACTIVE)
        for user_activity in user_activities:
            user_activity.status = UserActivity.CANCELLED
            user_activity.put()
        self.get_event().status = Event.CANCELLED
        self.get_event().put()
        return True




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
        #Count the number of companions first to handle the eventual consistency pattern for ndb
        companion_count = self.companion_count() + 1
        user_info = models.User.get_by_id(long(user_id))
        user_activity = UserActivity(user=user_info.key,
                                     activity=self._event.key)
        user_activity.put()
        #An activity will be marked as FORMED_OPEN if it satisfies the minm number of people required requirement
        if self._event.status == Event.FORMING:
            if self._can_complete(companion_count):
                self._event.status = Event.FORMED_OPEN
                self._event.put()
                self._on_event_formation()
        return True, message

    def join_flex_interest(self,user_id,**kwargs):
        self._event.type = Event.EVENT_TYPE_SPECIFIC_INTEREST
        if 'min_number_of_people_to_join' in kwargs and kwargs['min_number_of_people_to_join'] != "":
            self._event.min_number_of_people_to_join = kwargs['min_number_of_people_to_join']
        if 'max_number_of_people_to_join' in  kwargs and kwargs['max_number_of_people_to_join'] != "":
            self._event.max_number_of_people_to_join = kwargs['max_number_of_people_to_join']
        if 'note' in kwargs and kwargs['note'] != "":
            self._event.note = kwargs['note']
        if 'meeting_place' in kwargs and kwargs['meeting_place'] != "":
            self._event.meeting_place = kwargs['meeting_place']
        if 'activity_location' in kwargs and kwargs['activity_location'] != "":
            self._event.meeting_place = kwargs['activity_location']
        self._event.put()
        self.connect(user_id)

    def spots_remaining(self):
        if self._event.max_number_of_people_to_join == 'No limit':
            return self._event.max_number_of_people_to_join
        max_count = int(self._event.max_number_of_people_to_join.split()[0])
        return max_count - self.companion_count()

    def _can_complete(self,companion_count):
        min_count = int(self._event.min_number_of_people_to_join.split()[0])
        return min_count <= companion_count

    def mark_expired(self):
        self._change_status(Event.EXPIRED)

    def can_join(self, userId):
        #First check the status
        if self.expires_in() == Event.EXPIRED or self._event.status in Event.NON_EDITABLE_STATUS_CHOICES:
            return False, "Event is already expired/cancelled or closed"
        #Are there any activities with this user and this activity?
        user_info = models.User.get_by_id(long(userId))
        if self._event.username == user_info.username:
            return False, "You yourself created this activity."
        user_activity = UserActivity.get_by_user_activity(user_info.key, self._event.key)
        if user_activity:
            return False, "You have already joined this activity."
        #Now check if there are spots remaining
        elif self._event.max_number_of_people_to_join == 'No Limit':
            return True, "Success"
        else:
            max_count = int(self._event.max_number_of_people_to_join.split()[0])
            if self.companion_count() < max_count:
                return True, "Success"
            return False, "This activity is full."

    def status(self):
        return self._event.status

    def get_event(self):
        return self._event


    def expires_in(self):
        if self._event.status == Event.EXPIRED:
            return Event.EXPIRED
        else:
            activity_expiration_time = self._calculate_activity_expiration_time()
            now = datetime.utcnow()
            if now < activity_expiration_time:
                return  activity_expiration_time - now
            return Event.EXPIRED

    def _change_status(self,new_status):
        self._event.status = new_status
        self._event.put()

    def companion_count(self):
        companions = UserActivity.query(UserActivity.activity == self._event.key, UserActivity.status == UserActivity.ACTIVE).count()
        logging.info(companions)
        return companions

    def get_all_companions(self):
        return UserActivity.query(UserActivity.activity == self._event.key, UserActivity.status == UserActivity.ACTIVE).fetch(projection = [UserActivity.user])

    def get_all_participants(self):
        companions = self.get_all_companions()
        activity_user = models.User.get_by_username(self.get_event().username)
        companions.append(activity_user)
        return companions

    def _calculate_activity_expiration_time(self):
        if self._event.start_time is not None and self._event.start_time != "":
            return self._event.start_time
        elif self._event.expiration is not None and self._event.expiration != "":
            expiration_time = int(str(self._event.expiration))
            return self._event.date_entered + timedelta(minutes=expiration_time)

    #TODO Recheck these calculations
    def _on_event_formation(self):
        #Queue it for life cycle management
        if os.environ.get('ENV_TYPE') is None:
            if self._event.start_time is not None and self._event.start_time != "":
                task_execution_time = self._event.start_time - timedelta(minutes=5)
            if self._event.expiration is not None and self._event.expiration != "":
                task_execution_time = datetime.utcnow() + timedelta(minutes=5)
            goTask = Task(eta=task_execution_time, url='/activity_life_cycle/',method='GET',params={'activity': self._event.key.urlsafe()})
            goTask.add('activityLifeCycle')


