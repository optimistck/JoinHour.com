__author__ = 'aparbane'
from src.joinhour.models.interest import Interest
from google.appengine.ext import ndb
from  datetime import datetime
from datetime import timedelta
from google.appengine.api import taskqueue
from google.appengine.api.taskqueue import Task
import os


class InterestManager(object):

    @classmethod
    def create_interest(cls,**kwargs):
        interest = Interest(category = kwargs['category'],
                            duration = kwargs['duration'],
                            expiration = kwargs['expiration'],
                            username = kwargs['username'],
                            building_name = kwargs['building_name'],
                            date_entered = datetime.utcnow()

        )
        interest.put()
        if os.environ.get('ENV_TYPE') != 'TEST':
            task = Task(url='/match_maker/',method='GET',params={'interest': interest.key.urlsafe()})
            task.add('matchmaker')
        return interest


    @classmethod
    def get(cls,key):
        return InterestManager(key)

    def __init__(self,key):
        self._interest = ndb.Key(urlsafe=key).get()

    def get_interest(self):
        return self._interest

    def expires_in(self):
        if self._interest.status == Interest.EXPIRED:
            return Interest.EXPIRED
        else:
            expiration_time = int(str(self._interest.expiration))
            now = datetime.utcnow()
            if now < (self._interest.date_entered + timedelta(minutes=expiration_time)):
                return  (self._interest.date_entered + timedelta(minutes=expiration_time)) - now
            return Interest.EXPIRED