__author__ = 'aparbane'
from google.appengine.ext import ndb

class Activity(ndb.Model):

    INITIATED = 'INITIATED'
    FORMING = 'FORMING'
    EXPIRED = 'EXPIRED'
    COMPLETE = 'COMPLETE'

    category = ndb.StringProperty()
    min_number_of_people_to_join = ndb.StringProperty()
    max_number_of_people_to_join = ndb.StringProperty()
    duration = ndb.StringProperty()
    expiration = ndb.StringProperty()
    note = ndb.StringProperty()
    date_entered = ndb.DateTimeProperty(auto_now_add=True)
    username = ndb.StringProperty()
    ip = ndb.StringProperty()
    headcount = ndb.IntegerProperty(default=0)
    status = ndb.StringProperty(default=INITIATED,choices=[INITIATED,FORMING,EXPIRED,COMPLETE])


    @classmethod
    def query_activity(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key).order(-cls.date_entered)






