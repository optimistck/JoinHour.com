__author__ = 'aparbane'
from google.appengine.ext import ndb
from protorpc import remote, messages
from protorpc import message_types
from src.joinhour.models.feedback import CompanionShipRating


class UpdateRatingRequest(messages.Message):
    key = messages.StringField(1, required=True)
    rating = messages.StringField(2, required=True)


class CompanionShipRatingService(remote.Service):

    @remote.method(UpdateRatingRequest, message_types.VoidMessage)
    def update_rating(self, request):
        #First query the companionship rating
        companion_ship_rating = ndb.Key(urlsafe=request.key).get()
        #Now update the rating
        companion_ship_rating.rating = request.rating
        companion_ship_rating.put()
        return message_types.VoidMessage()


