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
    interest_owner = ndb.KeyProperty(kind=User,name='user',required=True)
    date_entered = ndb.DateTimeProperty(required=True)


    @classmethod
    def get_by_approver(approver_user):
        return cls.query(cls.activity == Event.EVENT_TYPE_SPECIFIC_INTEREST,cls.category == category,cls.status.IN(Event.JOINABLE_STATUS_CHOICES)).fetch()








