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
                            requester = kwargs['requester_key']
        )
        request.put()
        return True,request

    @classmethod
    def get(cls,key):

        return RequestManager(key)


    def __init__(self,key):
        self._request = ndb.Key(urlsafe=key).get()


    def accept(self):
        event_manager = EventManager.get(self._request.activity.urlsafe())
        status,message = event_manager.connect(self._request.requester.id())
        if status :
            self._request.status = Request.ACCEPTED
            self._request.put()
            return True,"Accepted & Connected"
        else:
            return False,message


    def reject(self):
        self._request.status = Request.REJECTED
        self._request.put()

    def cancel(self):
        self._request.status = Request.CANCELLED
        self._request.put()

    def can_cancel(self,user):
        if self._request.requester.get().username == user:
            return self._request.status == Request.INITIATED
        return False;

    def can_accept(self,user):
        if self._request.activity.get().username == user:
            return self._request.status == Request.INITIATED
        return False;

    def can_reject(self,user):
        if self._request.activity.get().username == user:
            return self._request.status == Request.INITIATED
        return False;

    def get_request(self):
        return self._request




