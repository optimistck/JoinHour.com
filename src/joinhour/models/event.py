__author__ = 'ashahab'
from google.appengine.ext import ndb

class Event(ndb.Model):



    INITIATED = 'INITIATED'
    FORMING = 'FORMING'
    EXPIRED = 'EXPIRED'
    COMPLETE = 'COMPLETE'
    COMPLETE_MATCH_FOUND = 'COMPLETE_MATCH_FOUND'
    COMPLETE_JOINED = 'COMPLETE_JOINED'
    COMPLETE_CONVERTED = 'COMPLETE_CONVERTED'
    EVENT_TYPE_ACTIVITY = 'ACTIVITY'
    EVENT_TYPE_INTEREST = 'INTEREST'
    STATUS_CHOICES = [INITIATED,FORMING,EXPIRED,COMPLETE,COMPLETE_MATCH_FOUND,COMPLETE_JOINED,COMPLETE_CONVERTED]
    category = ndb.StringProperty()
    date_entered = ndb.DateTimeProperty()
    username = ndb.StringProperty()
    duration = ndb.StringProperty()
    expiration = ndb.StringProperty()
    status = ndb.StringProperty(default=INITIATED, choices = STATUS_CHOICES)
    building_name = ndb.StringProperty()
    note = ndb.StringProperty()
    type = ndb.StringProperty(default=EVENT_TYPE_ACTIVITY,choices= [EVENT_TYPE_ACTIVITY,EVENT_TYPE_INTEREST])
    min_number_of_people_to_join = ndb.StringProperty()
    max_number_of_people_to_join = ndb.StringProperty()

    @classmethod
    def query_all_active_events(cls):
        return cls.query(cls.status.IN([INITIATED, FORMING]))

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

    @classmethod
    def get_activities_by_building(cls,building_name):
        return cls.query(cls.building_name == building_name, cls.type == Event.EVENT_TYPE_ACTIVITY).order(-cls.date_entered).fetch()

    @classmethod
    def get_interests_by_building(cls,building_name):
        return cls.query(cls.building_name == building_name, cls.type == Event.EVENT_TYPE_INTEREST).order(-cls.date_entered).fetch()

    @classmethod
    def get_active_interests_by_building_not_mine(cls, building, username):
        return cls.query(cls.type == Event.EVENT_TYPE_INTEREST,cls.building_name == building, Event.username != username,
                         cls.status.IN([Event.FORMING, Event.INITIATED])).fetch()

    @classmethod
    def get_active_interests_by_category(cls, category):
        return cls.query(cls.type == Event.EVENT_TYPE_INTEREST,cls.category == category, cls.status.IN([Event.FORMING, Event.INITIATED])).fetch()

    @classmethod
    def get_active_interests_by_category_and_building(cls, category, building_name):
        return cls.query(cls.type == Event.EVENT_TYPE_INTEREST,cls.category == category, cls.building_name == building_name,
                         cls.status.IN([Event.INITIATED, Event.FORMING])).fetch()

    @classmethod
    def get_active_activities_by_category_and_building(cls,category,building_name):
        return cls.query(cls.type == Event.EVENT_TYPE_ACTIVITY,cls.category == category,cls.building_name == building_name,cls.status.IN([Event.INITIATED,Event.FORMING])).fetch()

    @classmethod
    def get_active_activities_by_category(cls,category):
        return cls.query(cls.type == Event.EVENT_TYPE_ACTIVITY,cls.category == category,cls.status.IN([Event.INITIATED,Event.FORMING])).fetch()







