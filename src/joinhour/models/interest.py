__author__ = 'aparbane'
from event import Event

class Interest(Event):

    @classmethod
    def get_active_interests_by_building_not_mine(cls, building, username):
        return cls.query(cls.building_name == building, Interest.username != username,
                         cls.status.IN([Interest.FORMING, Interest.INITIATED])).fetch()

    @classmethod
    def get_active_interests_by_category(cls, category):
        return cls.query(cls.category == category, cls.status.IN([Interest.FORMING, Interest.INITIATED])).fetch()

    @classmethod
    def get_active_interests_by_category_and_building(cls, category, building_name):
        return cls.query(cls.category == category, cls.building_name == building_name,
                         cls.status.IN([Interest.INITIATED, Interest.FORMING])).fetch()

    @classmethod
    def get_interests_by_building(cls, building_name):
        return cls.query(cls.building_name == building_name).order(-cls.date_entered).fetch()





