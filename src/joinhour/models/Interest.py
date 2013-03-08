__author__ = 'aparbane'
from google.appengine.ext import ndb
class Interest(ndb.Model):
    interest = ndb.StringProperty()
    date_entered = ndb.DateTimeProperty(auto_now_add=True)
    username = ndb.StringProperty()
    duration = ndb.IntegerProperty()
    expiration = ndb.IntegerProperty()

    @classmethod
    def query_interest(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key).order(-cls.date_entered)
