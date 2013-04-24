__author__ = 'aparbane'
from google.appengine.ext import ndb
from activity_interest_summary import ActivityInterestSummary

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
    date_entered = ndb.DateTimeProperty()
    username = ndb.StringProperty()
    ip = ndb.StringProperty()
    status = ndb.StringProperty(default=INITIATED,choices=[INITIATED,FORMING,EXPIRED,COMPLETE])
    building_name = ndb.StringProperty()

    def get_summary(self):
        return ActivityInterestSummary(
            category=self.category,
            date_entered=self.date_entered,
            username=self.username,
            duration=self.duration,
            expiration=self.expiration,
            status=self.status,
            building_name=self.building_name,
            min_number_of_people_to_join=self.min_number_of_people_to_join,
            max_number_of_people_to_join=self.max_number_of_people_to_join,
            ip=self.ip,
            headcount=self.headcount
        )

    @classmethod
    def query_paged(cls, building_name, user_info, curs):
        return Activity.query(Activity.building_name == building_name, Activity.username != user_info.username)\
            .fetch_page(5, start_cursor=curs).order(cls._key)

    @classmethod
    def query_activity(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key).order(-cls.date_entered)

    @classmethod
    def query_all_unexpired_activity(cls):
        return cls.query(cls.status != Activity.EXPIRED)
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
    def get_active_activities_by_category(cls,category):
        return cls.query(cls.category == category,cls.status.IN([Activity.INITIATED,Activity.FORMING])).fetch()

    @classmethod
    def get_active_activities_by_category_and_building(cls,category,building_name):
        return cls.query(cls.category == category,cls.building_name == building_name,cls.status.IN([Activity.INITIATED,Activity.FORMING])).fetch()


    @classmethod
    def get_activities_by_building(cls,building_name):
        return cls.query(cls.building_name == building_name).order(-cls.date_entered).fetch()






