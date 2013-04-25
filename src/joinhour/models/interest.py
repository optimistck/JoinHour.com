__author__ = 'aparbane'
from google.appengine.ext import ndb

class Interest(ndb.Model):
    INITIATED = 'INITIATED'
    FORMING = 'FORMING'
    EXPIRED = 'EXPIRED'
    COMPLETE_MATCH_FOUND = 'COMPLETE_MATCH_FOUND'
    COMPLETE_JOINED = 'COMPLETE_JOINED'
    COMPLETE_CONVERTED = 'COMPLETE_CONVERTED'
    category = ndb.StringProperty()
    date_entered = ndb.DateTimeProperty()
    username = ndb.StringProperty()
    duration = ndb.StringProperty()
    expiration = ndb.StringProperty()
    status = ndb.StringProperty(default=INITIATED,choices=[INITIATED,FORMING,EXPIRED,COMPLETE_MATCH_FOUND,COMPLETE_JOINED,COMPLETE_CONVERTED])
    building_name = ndb.StringProperty()

    @classmethod
    def query_interest(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key).order(-cls.date_entered)

    @classmethod
    def query_all_unexpired_interest(cls):
        return cls.query(cls.status.IN([Interest.FORMING,Interest.INITIATED]))

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
    def get_by_key(cls,key):
        return cls.query(cls.key == key).get()

    @classmethod
    def get_active_interests_by_building_not_mine(cls,building, username):
        return cls.query(cls.building_name == building, Interest.username != username, cls.status.IN([Interest.FORMING,Interest.INITIATED])).fetch()

    @classmethod
    def get_active_interests_by_category(cls,category):
        return cls.query(cls.category == category,cls.status.IN([Interest.FORMING,Interest.INITIATED])).fetch()

    @classmethod
    def get_active_interests_by_category_and_building(cls,category,building_name):
        return cls.query(cls.category == category,cls.building_name == building_name,cls.status.IN([Interest.INITIATED,Interest.FORMING])).fetch()

    @classmethod
    def get_interests_by_building(cls,building_name):
        return cls.query(cls.building_name == building_name).order(-cls.date_entered).fetch()





