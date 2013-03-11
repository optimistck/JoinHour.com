__author__ = 'aparbane'
from src.joinhour.models.interest import Interest
from google.appengine.ext import ndb
from  datetime import datetime
from datetime import timedelta
class InterestManager(object):

    @classmethod
    def create_interest(cls,**kwargs):
        interest = Interest(parent=ndb.Key("InterestKey", kwargs['building_name']),
                            category = kwargs['category'],
                            duration = kwargs['duration'],
                            expiration = kwargs['expiration'],
                            username = kwargs['username']

        )
        interest.put()

    @classmethod
    def get(cls,interestId):
        return InterestManager(interestId)

    def __init__(self,interestId):
        self._interest = Interest.get_by_id(interestId,parent=ndb.Key("InterestKey", 'building_name'))

    def expires_in(self):
        if self._interest.status == Interest.EXPIRED:
            return Interest.EXPIRED
        else:
            expiration_time = int(str(self._interest.expiration))
            now = datetime.now()
            if now < (self._interest.date_entered + timedelta(minutes=expiration_time)):
                return  (self._interest.date_entered + timedelta(minutes=expiration_time)) - now
            return Interest.EXPIRED