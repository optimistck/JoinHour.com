__author__ = 'ashahab'
from google.appengine.ext import ndb

class Event(ndb.Model):


    #Event States


    INITIATED = 'INITIATED'
    FORMING = 'FORMING'
    EXPIRED = 'EXPIRED'
    COMPLETE = 'COMPLETE'
    FORMED_OPEN = 'FORMED_OPEN'
    FORMED_INITIATED = 'FORMED_INITIATED'
    COMPLETE_MATCH_FOUND = 'COMPLETE_MATCH_FOUND'
    COMPLETE_JOINED = 'COMPLETE_JOINED'
    COMPLETE_CONVERTED = 'COMPLETE_CONVERTED'
    CANCELLED = 'CANCELLED'
    CLOSED = 'CLOSED'
    COMPLETE_NEEDS_FEEDBACK = 'COMPLETE_NEEDS_FEEDBACK'



    #Event Types
    EVENT_TYPE_SPECIFIC_INTEREST = 'INTEREST_SPECIFIC'
    EVENT_TYPE_FLEX_INTEREST = 'INTEREST_FLEX'

    #Misc Constants

    STATUS_CHOICES = [FORMING,FORMED_OPEN,EXPIRED,CANCELLED,FORMED_INITIATED,COMPLETE_NEEDS_FEEDBACK,CLOSED]
    NON_EDITABLE_STATUS_CHOICES = [EXPIRED,CANCELLED,FORMED_INITIATED,COMPLETE_NEEDS_FEEDBACK,CLOSED]
    JOINABLE_STATUS_CHOICES = [FORMING,FORMED_OPEN]
    #activity_category
    category = ndb.StringProperty(required=True)
    #date the activity is entered
    date_entered = ndb.DateTimeProperty(required=True)
    #activity owner user name.
    #TODO: This should be a reference to user model
    username = ndb.StringProperty(required=True)
    #TODO This should be a reference to building/geohood model
    building_name = ndb.StringProperty(required=True)
    #duration
    duration = ndb.StringProperty()
    #this is to specify the time the user is willing to wait for
    expiration = ndb.StringProperty()
    #activity status
    status = ndb.StringProperty(default=FORMING, choices = STATUS_CHOICES)
    #TODO Any additional notes specified by the user
    note = ndb.StringProperty()
    #interest type - Flex Interest or Specific
    type = ndb.StringProperty(default=EVENT_TYPE_SPECIFIC_INTEREST,choices= [EVENT_TYPE_SPECIFIC_INTEREST,EVENT_TYPE_FLEX_INTEREST])
    #Min number of participants needed to start
    min_number_of_people_to_join = ndb.StringProperty()
    #Max number of participants this interest can accommodate
    max_number_of_people_to_join = ndb.StringProperty()
    #meeting place where this interest will happen
    meeting_place = ndb.StringProperty()
    #activity location
    activity_location = ndb.StringProperty()
    #start_time at which the activity will start. This is mutually exclusive with the attribute expiration
    start_time = ndb.DateTimeProperty()

    @classmethod
    def query_all_active_events(cls):
        return cls.query(cls.status.IN([Event.FORMING]))

    @classmethod
    def query_all_active_events_by_building(cls,building_name):
        return cls.query(cls.status.IN([Event.FORMING]), cls.building_name == building_name).fetch()


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
        return cls.query(cls.building_name == building_name, cls.type == Event.EVENT_TYPE_SPECIFIC_INTEREST).order(-cls.date_entered).fetch()

    @classmethod
    def get_latest_forming_activities(cls, user, building_name, date):
        return cls.query(cls.building_name == building_name, cls.username == user, cls.date_entered > date, cls.status == Event.FORMING).fetch(projection=Event.date_entered);

    @classmethod
    def get_interests_by_building(cls,building_name):
        return cls.query(cls.building_name == building_name, cls.type == Event.EVENT_TYPE_FLEX_INTEREST).order(-cls.date_entered).fetch()


    @classmethod
    def get_active_interests_by_category(cls, category):
        return cls.query(cls.type == Event.EVENT_TYPE_FLEX_INTEREST,cls.category == category, cls.status.IN(Event.JOINABLE_STATUS_CHOICES)).fetch()

    @classmethod
    def get_active_interests_by_category_and_building(cls, category, building_name):
        return cls.query(cls.type == Event.EVENT_TYPE_FLEX_INTEREST,cls.category == category, cls.building_name == building_name,
                         cls.status.IN(Event.JOINABLE_STATUS_CHOICES)).fetch()

    @classmethod
    def get_active_activities_by_category_and_building(cls,category,building_name):
        return cls.query(cls.type == Event.EVENT_TYPE_SPECIFIC_INTEREST,cls.category == category,cls.building_name == building_name,cls.status.IN(Event.JOINABLE_STATUS_CHOICES)).fetch()

    @classmethod
    def get_active_activities_by_category(cls,category):
        return cls.query(cls.type == Event.EVENT_TYPE_SPECIFIC_INTEREST,cls.category == category,cls.status.IN(Event.JOINABLE_STATUS_CHOICES)).fetch()







