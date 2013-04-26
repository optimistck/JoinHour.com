__author__ = 'aparbane'
from google.appengine.ext import ndb

from event import Event


class Interest(Event):



    COMPLETE_MATCH_FOUND = 'COMPLETE_MATCH_FOUND'
    COMPLETE_JOINED = 'COMPLETE_JOINED'
    COMPLETE_CONVERTED = 'COMPLETE_CONVERTED'
    STATUS_CHOICES = [Event.INITIATED,Event.FORMING,Event.EXPIRED,COMPLETE_MATCH_FOUND,COMPLETE_JOINED,COMPLETE_CONVERTED]
    #Just a monkey patch since _init_ way of overriding is not supported when I extend from ndb model
    status = ndb.StringProperty(default=Event.INITIATED, choices = STATUS_CHOICES)
    @classmethod
    def get_active_interests_by_building_not_mine(cls, building, username):
        return cls.query(cls.building_name == building, Event.username != username,
                         cls.status.IN([Event.FORMING, Event.INITIATED])).fetch()

    @classmethod
    def get_active_interests_by_category(cls, category):
        return cls.query(cls.category == category, cls.status.IN([Event.FORMING, Event.INITIATED])).fetch()

    @classmethod
    def get_active_interests_by_category_and_building(cls, category, building_name):
        return cls.query(cls.category == category, cls.building_name == building_name,
                         cls.status.IN([Event.INITIATED, Event.FORMING])).fetch()

    @classmethod
    def get_interests_by_building(cls, building_name):
        return cls.query(cls.building_name == building_name).order(-cls.date_entered).fetch()







