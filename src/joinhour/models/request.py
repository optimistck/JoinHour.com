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
    activity = ndb.KeyProperty(kind=Event,name='activity')
    requester = ndb.KeyProperty(kind=User,name='user',required=True)
    date_entered = ndb.DateTimeProperty(required=True)

    @classmethod
    def can_initiate(cls,activity,requester):
        return  cls.query(cls.activity == activity,cls.requester==requester).get() is  None


    @classmethod
    def get_open_request(self,activity_owner):
        return cls.






