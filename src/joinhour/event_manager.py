__author__ = 'aparbane'

from  datetime import datetime
from datetime import timedelta
import os

from google.appengine.ext import ndb
from google.appengine.api.taskqueue import Task

from src.joinhour.models.event import Event
from src.joinhour.models.user_activity import UserActivity
from boilerplate import models


class EventManager(object):


    @classmethod
    def create_activity(cls,**kwargs):
        '''
        Creates a new event with the arguments specified.
        After creation Starts initiates the matchmaker task for finding a possible match and also initiates the event lifecycle task
        :param cls:
        :param kwargs:
        :return: The newly created event
        '''
        event = Event(category = kwargs['category'],
                            duration = kwargs['duration'],
                            expiration = kwargs['expiration'],
                            note = kwargs['note'],
                            min_number_of_people_to_join = kwargs['min_number_of_people_to_join'],
                            max_number_of_people_to_join = kwargs['max_number_of_people_to_join'],
                            username = kwargs['username'],
                            building_name = kwargs['building_name'],
                            date_entered = datetime.utcnow()
        )
        event.put()
        if os.environ.get('ENV_TYPE') is None:
            task = Task(url='/match_maker/',method='GET',params={'activity': event.key.urlsafe()})
            task.add('matchmaker')
            expiration_time = int(str(event.expiration))
            timezone_offset = datetime.now() - datetime.utcnow()
            task_execution_time = event.date_entered + timedelta(minutes=expiration_time) - timedelta(minutes=5) + timezone_offset
            goTask = Task(eta=task_execution_time, url='/activity_life_cycle/',method='GET',params={'event': event.key.urlsafe()})
            goTask.add('activityLifeCycle')
        return event

    @classmethod
    def create_activity_from_interest(cls, **kwargs):
        '''
        Creates a new activity from an interest. Also joins the interest owner with the activity. The interest is marked as COMPLETE and the match table is populated.
        :param cls:
        :param kwargs:
        :return:
        '''
        interest = ndb.Key(urlsafe=kwargs['interest_id']).get()
        if EventManager.get(interest.key.urlsafe()).expires_in() == Event.EXPIRED or Event.status == Event.COMPLETE:
            return False, "Cannot create activity from an expired or completed interest"
        #Create the activity
        event = EventManager.create_activity(
                                        building_name=interest.building_name,category=interest.category,
                                        duration=interest.duration,expiration = interest.expiration,
                                        username = kwargs['username'],note = kwargs['note'],
                                        ip = kwargs['ip'],
                                        min_number_of_people_to_join = kwargs['min_number_of_people_to_join'],
                                        max_number_of_people_to_join = kwargs['max_number_of_people_to_join'])
        #mark interest complete
        interest.status = Event.COMPLETE_JOINED
        user = models.User.get_by_username(interest.username)
        success, message = EventManager.get(event.key.urlsafe()).connect(user.key.id())
        interest.put()
         #Notify interest owner
        return success, message, user.key.id(), event.key.urlsafe()

    @classmethod
    def create_interest(cls,**kwargs):
        event = Event(category = kwargs['category'],
                            duration = kwargs['duration'],
                            expiration = kwargs['expiration'],
                            username = kwargs['username'],
                            building_name = kwargs['building_name'],
                            note = kwargs['note'],
                            type = Event.EVENT_TYPE_INTEREST,
                            date_entered = datetime.utcnow()

        )
        event.put()
        if os.environ.get('ENV_TYPE') is None:
            task = Task(url='/match_maker/',method='GET',params={'interest': event.key.urlsafe()})
            task.add('matchmaker')
        return event

    @classmethod
    def get(cls,key):
        '''
        Returns a Handle to the activity manager for an activity key
        :param cls:
        :param key: ActivityKey
        :return:
        '''
        return EventManager(key)

    def __init__(self,key):
        self._event = ndb.Key(urlsafe=key).get()

    def can_leave(self):
        if self.expires_in() == Event.EXPIRED:
            return False, "You cannot leave an expired activity."
        if self._event.status == Event.COMPLETE:
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
        user_activity = UserActivity.get_by_user_activity(user_info.key, self._event.key)
        user_activity.key.delete()
        if not self._is_complete():
            if self.companion_count() > 0:
                self._event.status = Event.FORMING
            else:
                self._event.status = Event.INITIATED
            self._event.put()
        return True, "user " + user_info.username + " has been successfully removed from activity " + self._event.category

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
                                     activity=self._event.key)
        user_activity.put()
        #An activity will be marked as COMPLETE if it satisfies the minm number of people required requirement
        if self._event.status == Event.INITIATED or self._event.status == Event.FORMING:
            if self._is_complete():
                self._event.status = Event.COMPLETE
            else:
                self._event.status = Event.FORMING
            self._event.put()
        return True, message

    def spots_remaining(self):
        if self._event.max_number_of_people_to_join == 'No limit':
            return self._event.max_number_of_people_to_join
        max_count = int(self._event.max_number_of_people_to_join.split()[0])
        return max_count - self.companion_count()

    def _is_complete(self):
        min_count = int(self._event.min_number_of_people_to_join.split()[0])
        return min_count <= self.companion_count()

    def mark_expired(self):
        self._change_status(Event.EXPIRED)

    def can_join(self, userId):
        #First check the status
        if self.expires_in() == Event.EXPIRED:
            return False, "Event is already expired"
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
            expiration_time = int(str(self._event.expiration))
            now = datetime.utcnow()
            activity_creation_date = self._event.date_entered
            if now < (activity_creation_date + timedelta(minutes=expiration_time)):
                return  (activity_creation_date + timedelta(minutes=expiration_time)) - now
            return Event.EXPIRED

    def _change_status(self,new_status):
        self._event.status = new_status
        self._event.put()

    def companion_count(self):
        return UserActivity.query(UserActivity.activity == self._event.key).count()

    def get_all_companions(self):
        return UserActivity.query(UserActivity.activity == self._event.key).fetch(projection = [UserActivity.user])

    def get_all_participants(self):
        companions = self.get_all_companions()
        activity_user = models.User.get_by_username(self.get_event().username)
        companions.append(activity_user)
        return companions
