from src.joinhour.models.event import Event

__author__ = 'ashahab'
from google.appengine.api import memcache
from src.joinhour.models.user_activity import UserActivity
from boilerplate import models
from  datetime import datetime
from datetime import timedelta
from google.appengine.ext import ndb


class EventThrottler(object):
    FIVE_MINUTES = 5
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
        latest_activities = UserActivity.get_latest_activities(self._user.key, five_minutes_ago)
        #For each activity, find it, and
        numEvents = 0
        for user_activity in latest_activities:
            event = ndb.Key(urlsafe=user_activity.activity.urlsafe()).get()
            if event.status == Event.FORMING:
                numEvents += 1

        return numEvents

    def increment_activity_count(self):
        self.number_of_cached_events()
        return memcache.incr(self._user.username)

    def decrement_activity_count(self):
        self.number_of_cached_events()
        return memcache.decr(self._user.username)
