__author__ = 'apbanerjee'

from google.appengine.ext import ndb
from src.joinhour.models.event import Event
from boilerplate.models import User

class Request(ndb.Model):

    #States

    INITIATED = 'INITIATED'
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'
    EXPIRED = 'EXPIRED'
    CANCELLED = 'CANCELLED'
    STATES = [INITIATED,ACCEPTED,REJECTED,EXPIRED]
    #Attributes
    status = ndb.StringProperty(default=INITIATED, choices = STATES)
    activity = ndb.KeyProperty(kind=Event,name='activity',required=True)
    requester = ndb.KeyProperty(kind=User,name='user',required=True)
    date_entered = ndb.DateTimeProperty(required=True)
    activity_owner = ndb.ComputedProperty(lambda self: self.activity.get().username)

    @classmethod
    def can_initiate(cls,activity,requester):
        return  cls.query(cls.activity == activity,cls.requester==requester).get() is  None


    @classmethod
    def get_open_requests_for_owner(cls,activity_owner):
        return cls.query(cls.activity_owner == activity_owner).fetch()

    @classmethod
    def get_open_requests_for_activity(cls,activity):
        return cls.query(cls.activity == activity,cls.status == Request.INITIATED).fetch()

    @classmethod
    def can_cancel(cls,activity,requester):
        return cls.query(cls.activity == activity,cls.requester==requester,cls.status == Request.INITIATED) is not None






