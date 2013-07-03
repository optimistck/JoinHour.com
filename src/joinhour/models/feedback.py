__author__ = 'aparbane'

from google.appengine.ext import ndb

from src.joinhour.models.event import Event
from boilerplate.models import User


class ActivityFeedback(ndb.Model):

    OPEN = 'OPEN'
    CLOSED_WITHOUT_FEEDBACK = 'CLOSED_WITHOUT_FEEDBACK'
    CLOSED_WITH_FEEDBACK = 'CLOSED_WITH_FEEDBACK'
    activity = ndb.KeyProperty(kind=Event,name='activity',required=True)
    date_entered = ndb.DateTimeProperty(auto_now_add=True)
    status = ndb.StringProperty(default = OPEN,choices=[OPEN,CLOSED_WITHOUT_FEEDBACK,CLOSED_WITH_FEEDBACK])

class UserFeedback(ndb.Model):

    NEGATIVE = 'NEGATIVE'
    NEUTRAL = 'NEUTRAL'
    POSITIVE = 'POSITIVE'
    VERY_POSITIVE = 'VERY_POSITIVE'
    SUPER_POSITIVE = 'SUPER_POSITIVE'
    OPEN = 'OPEN'
    CLOSED_WITHOUT_FEEDBACK = 'CLOSED_WITHOUT_FEEDBACK'
    CLOSED_WITH_FEEDBACK = 'CLOSED_WITH_FEEDBACK'
    user = ndb.KeyProperty(kind=User,name='user')
    activity = ndb.KeyProperty(kind=Event,name='activity',required=True)
    activity_experience =  ndb.StringProperty(default=NEUTRAL,choices=[NEGATIVE,NEUTRAL,
                                                                                    POSITIVE,VERY_POSITIVE,SUPER_POSITIVE])
    status = ndb.StringProperty(default=OPEN,choices=[OPEN,CLOSED_WITHOUT_FEEDBACK,CLOSED_WITH_FEEDBACK])


class CompanionShipRating(ndb.Model):
    INAPPROPRIATE = 'INAPPROPRIATE'
    NO_SHOW = 'NO_SHOW'
    NEUTRAL = 'NEUTRAL'
    GOOD = 'GOOD'
    VERY_GOOD = 'VERY_GOOD'
    OUTSTANDING = 'OUTSTANDING'
    activity = ndb.KeyProperty(kind=Event,name='activity',required=True)
    rater = ndb.KeyProperty(kind=User,name='rater')
    activity_category = ndb.StringProperty()
    activity_date = ndb.DateTimeProperty(auto_now_add=True)
    ratee = ndb.KeyProperty(kind=User,name='ratee')
    rating = ndb.StringProperty(default = NEUTRAL,choices=[INAPPROPRIATE,NO_SHOW,NEUTRAL,GOOD,VERY_GOOD,OUTSTANDING])
    blacklist = ndb.BooleanProperty(default=False)


