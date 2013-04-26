__author__ = 'ashahab'
from google.appengine.ext import ndb

class Event(ndb.Model):
    INITIATED = 'INITIATED'
    FORMING = 'FORMING'
    EXPIRED = 'EXPIRED'
    COMPLETE = 'COMPLETE'
    category = ndb.StringProperty()
    date_entered = ndb.DateTimeProperty()
    username = ndb.StringProperty()
    duration = ndb.StringProperty()
    expiration = ndb.StringProperty()
    status = ndb.StringProperty(default=INITIATED, choices=[INITIATED, FORMING, EXPIRED, COMPLETE])
    building_name = ndb.StringProperty()

    @classmethod
    def query_all_unexpired(cls):
        return cls.query(cls.status != Event.EXPIRED)

    @classmethod
    def query_event(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key).order(-cls.date_entered)

    @classmethod
    def get_by_status(cls, status):
        return cls.query(cls.status == status).fetch()

    @classmethod
    def get_by_category(cls,category):
        return cls.query(cls.category == category).fetch()

    @classmethod
    def get_by_status_and_category(cls,category,status):
        return cls.query(cls.category == category,cls.status == status).fetch()

    @classmethod
    def get_by_key(cls, key):
        return cls.query(cls.key == key).get()