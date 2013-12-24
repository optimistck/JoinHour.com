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





