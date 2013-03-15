__author__ = 'aparbane'
from google.appengine.ext import ndb
from webapp2_extras.appengine.auth.models import User
from src.joinhour.models.activity import Activity
from src.joinhour.models.interest import Interest


class Match(ndb.Model):

    NEW_MATCH = 'NEW_MATCH'
    NOTIFIED = 'NOTIFIED'
    interest = ndb.KeyProperty(kind=Interest,
                               name='interest')
    activity = ndb.KeyProperty(kind=Activity,
                               name='activity')
    match_found_date = ndb.DateTimeProperty(auto_now_add=True)
    status = ndb.StringProperty(default=NEW_MATCH,choices=[NEW_MATCH,NOTIFIED])
    match_type = ndb.StringProperty()

    @classmethod
    def already_tested_for_match(cls, activity,interest):
        return cls.query(cls.activity==activity,cls.interest==interest).get()
