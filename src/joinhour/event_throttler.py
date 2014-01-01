from src.joinhour.models.event import Event

__author__ = 'ashahab'
from google.appengine.api import memcache
from src.joinhour.models.user_activity import UserActivity
from boilerplate import models
from  datetime import datetime
from datetime import timedelta
from google.appengine.ext import ndb


class EventThrottler(object):
    # changed from 5 to 10. No more than 3 events can be set in 10 minutes.
    FIVE_MINUTES = 10
    CONFIG_TIME = FIVE_MINUTES

    @classmethod
    def get(cls,username):
        '''
        Returns a Handle to the event manager for an event
        :param cls:
        :param key: ActivityKey
        :return:
        '''
        return EventThrottler(username)

    def __init__(self,username):
        self._user = models.User.get_by_username(username)

    def number_of_cached_events(self):
        count = memcache.get(self._user.username)
        if count is None:
            count = self.number_of_events()
            memcache.add(self._user.username, count, self.CONFIG_TIME * 60)
        return count

    def number_of_events(self):
        #Get number of FORMING and events from User activity created in the last 5 minutes
        now = datetime.now()
        five_minutes_ago = now - timedelta(minutes=self.CONFIG_TIME)

        #For each activity, find it, and
        events = Event.get_latest_forming_activities(self._user.username, self._user.building, five_minutes_ago)
        return len(events)

    def increment_activity_count(self):
        self.number_of_cached_events()
        return memcache.incr(self._user.username)

    def decrement_activity_count(self):
        self.number_of_cached_events()
        return memcache.decr(self._user.username)
