__author__ = 'aparbane'
from src.joinhour.models.interest import Interest
from google.appengine.ext import ndb
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