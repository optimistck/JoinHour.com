__author__ = 'aparbane'
from google.appengine.ext import ndb
class Interest(ndb.Model):
    INITIATED = 'INITIATED'
    FORMING = 'FORMING'
    EXPIRED = 'EXPIRED'
    COMPLETE = 'COMPLETE'
    interest = ndb.StringProperty()
    date_entered = ndb.DateTimeProperty(auto_now_add=True)
    username = ndb.StringProperty()
    duration = ndb.IntegerProperty()
    expiration = ndb.IntegerProperty()
    status = ndb.StringProperty(default=INITIATED,choices=[INITIATED,FORMING,EXPIRED,COMPLETE])

    @classmethod
    def query_interest(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key).order(-cls.date_entered)

