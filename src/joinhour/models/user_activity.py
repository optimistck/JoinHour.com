__author__ = 'ashahab'
from google.appengine.ext import ndb
from webapp2_extras.appengine.auth.models import User
from src.joinhour.models.event import Event


class UserActivity(ndb.Model):

    ACTIVE = 'ACTIVE'
    CANCELLED = 'CANCELLED'
    user = ndb.KeyProperty(kind=User,
                           name='user')
    activity = ndb.KeyProperty(kind=Event,
                               name='activity')

    date_entered = ndb.DateTimeProperty(auto_now_add=True)

    status = ndb.StringProperty(default=ACTIVE, choices=[ACTIVE,CANCELLED])

    @classmethod
    def query_user_activity(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key).order(-cls.date_entered)

    @classmethod
    def get_users_for_activity(cls, activity):
        return cls.query(cls.activity == activity, cls.status == UserActivity.ACTIVE).fetch()

    @classmethod
    def get_by_user_activity(cls, user, activity):
        return cls.query(cls.user == user, cls.activity == activity).get()

    @classmethod
    def get_latest_activities(cls, user, date):
        return cls.query(cls.user == user, cls.date_entered > date, cls.status == UserActivity.ACTIVE).fetch();