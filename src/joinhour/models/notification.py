from boilerplate.models import User
from src.joinhour.models.event import Event

__author__ = 'aparbane'

from google.appengine.ext import ndb

class Notification(ndb.Model):

    NEW_COMPANION = 'NEW_COMPANION'
    GO_NOTIFICATION = 'GO_NOTIFICATION'
    FINAL_READINESS = 'FINAL_READINESS'
    REQUEST_TO_JOIN = 'REQUEST_TO_JOIN'

    type = ndb.StringProperty(required=True,choices= [NEW_COMPANION,GO_NOTIFICATION,FINAL_READINESS,REQUEST_TO_JOIN])
    event = ndb.KeyProperty(kind=Event,name='event',required=True)
    user = ndb.KeyProperty(kind=User,name='user',required=True)