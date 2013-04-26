__author__ = 'aparbane'
from google.appengine.ext import ndb
from event import Event

class Activity(Event):



    min_number_of_people_to_join = ndb.StringProperty()
    max_number_of_people_to_join = ndb.StringProperty()
    note = ndb.StringProperty()
    ip = ndb.StringProperty()

    @classmethod
    def query_paged(cls, building_name, user_info, curs):
        return Activity.query(Activity.building_name == building_name, Activity.username != user_info.username)\
            .fetch_page(5, start_cursor=curs).order(cls._key)

    @classmethod
    def get_active_activities_by_category(cls,category):
        return cls.query(cls.category == category,cls.status.IN([Activity.INITIATED,Activity.FORMING])).fetch()

    @classmethod
    def get_active_activities_by_category_and_building(cls,category,building_name):
        return cls.query(cls.category == category,cls.building_name == building_name,cls.status.IN([Activity.INITIATED,Activity.FORMING])).fetch()

    @classmethod
    def get_activities_by_building(cls,building_name):
        return cls.query(cls.building_name == building_name).order(-cls.date_entered).fetch()








