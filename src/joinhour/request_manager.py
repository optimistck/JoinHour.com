__author__ = 'apbanerjee'

from google.appengine.ext import ndb
from src.joinhour.models.request import Request
from src.joinhour.event_manager import EventManager
from  datetime import datetime


class RequestManager(object):

    @classmethod
    def initiate(cls,**kwargs):

        '''
        :param cls:
        :param kwargs:
        :return:
        '''

        request = Request(activity = kwargs['activity_key'],
                            date_entered = datetime.utcnow(),
                            interest_owner = kwargs['interest_owner_key']
        )
        request.put()
        return request

    @classmethod
    def get(cls,key):

        return RequestManager(key)


    def __init__(self,key):
        self._request = ndb.Key(urlsafe=key).get()


    def accept(self,user):
        event_manager = EventManager.get(self._request.activity.urlsafe())
        event_manager.connect(self._request.interest_owner)
        self._request.status = Request.ACCEPTED
        self._request.put()

    def reject(self):
        self._request.status = Request.REJECTED
        self._request.put()

    def cancel(self):
        self._request.status = Request.CANCELLED
        self._request.put()

    def can_cancel(self,user):
        return self._request.status == Request.INITIATED

    def can_accept(self,user):
        return self._request.status == Request.INITIATED

    def can_reject(self,user):
        return self._request.status == Request.INITIATED




