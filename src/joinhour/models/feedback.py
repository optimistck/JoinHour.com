__author__ = 'aparbane'

from google.appengine.ext import ndb
from boilerplate.models import User
from src.joinhour.models.activity import Activity

class ActivityFeedback(ndb.Model):

    OPEN = 'OPEN'
    CLOSED_WITHOUT_FEEDBACK = 'CLOSED_WITHOUT_FEEDBACK'
    CLOSED_WITH_FEEDBACK = 'CLOSED_WITH_FEEDBACK'
    activity = ndb.KeyProperty(kind=Activity,name='activity',required=True)
    date_entered = ndb.DateTimeProperty(auto_now_add=True)
    status = ndb.StringProperty(default = OPEN,choices=[OPEN,CLOSED_WITHOUT_FEEDBACK,CLOSED_WITH_FEEDBACK])

class UserFeedback(ndb.Model):

    NEGATIVE = 'NEGATIVE'
    NEUTRAL = 'NEUTRAL'
    POSITIVE = 'POSITIVE'
    VERY_POSITIVE = 'VERY_POSITIVE'
    SUPER_POSITIVE = 'SUPER_POSITIVE'
    user = ndb.KeyProperty(kind=User,name='user')
    activity_category = ndb.StringProperty()
    activity_date = ndb.DateTimeProperty(auto_now_add=True)
    activity_experience =  ndb.StringProperty(default=NEUTRAL,choices=[NEGATIVE,NEUTRAL,
                                                                                    POSITIVE,VERY_POSITIVE,SUPER_POSITIVE])


class CompanionShipRating(ndb.Model):
    INAPPROPRIATE = 'INAPPROPRIATE'
    NO_SHOW = 'NO_SHOW'
    NEUTRAL = 'NEUTRAL'
    GOOD = 'GOOD'
    VERY_GOOD = 'VERY_GOOD'
    OUTSTANDING = 'OUTSTANDING'
    rater = ndb.KeyProperty(kind=User,name='user')
    activity_category = ndb.StringProperty()
    activity_date = ndb.DateTimeProperty(auto_now_add=True)
    ratee = ndb.KeyProperty(kind=User,name='user')
    rating = ndb.StringProperty(default = NEUTRAL,choices=[INAPPROPRIATE,NO_SHOW,NEUTRAL,GOOD,VERY_GOOD,OUTSTANDING])
    blacklist = ndb.BooleanProperty(default=False)

