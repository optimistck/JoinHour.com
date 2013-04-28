from src.joinhour.models.event import Event

__author__ = 'aparbane'
from google.appengine.ext import ndb


class Match(ndb.Model):

    NEW_MATCH = 'NEW_MATCH'
    NOTIFIED = 'NOTIFIED'
    interest = ndb.KeyProperty(kind=Event,
                               name='interest')
    activity = ndb.KeyProperty(kind=Event,
                               name='activity')
    match_found_date = ndb.DateTimeProperty(auto_now_add=True)



    @classmethod
    def already_tested_for_match(cls, activity,interest):
        return cls.query(cls.activity==activity,cls.interest==interest).get()
