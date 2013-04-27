from UserString import MutableString
from src.joinhour.models.event import Event

__author__ = 'aparbane'

from src.joinhour.event_manager import EventManager
from boilerplate import models


def minute_format(timedelta):
    if timedelta != Event.EXPIRED and timedelta != Event.EXPIRED:
        total_seconds = int(timedelta.total_seconds())
        hours, remainder = divmod(total_seconds, 60*60)
        minutes, seconds = divmod(remainder, 60)
        if hours > 0:
            return str(hours) + ' hours ' + str(minutes) + ' minutes'
        else:
            return str(minutes) + ' minutes'
    return timedelta

def get_expiration_duration(key):
    return EventManager.get(key).expires_in()

def can_join(key, user_id):
    EventManager.get(key).can_join(user_id)[0]



def display_status(key,user_id):
    event_manager = EventManager.get(key)
    activity = event_manager.get_event()
    user = models.User.get_by_id(long(user_id))
    if user.username == activity.username:
        return activity.status
    else:
       can_join = event_manager.can_join(user_id)[0]
       if can_join:
           return "JOIN"
       else:
           return activity.status

def display_companions(key,user_id):
    event_manager = EventManager.get(key)
    activity = event_manager.get_event()
    user = models.User.get_by_id(long(user_id))
    is_owner = user.username == activity.username
    companions = event_manager.get_all_companions()
    message = MutableString()





def dateformat(value,format='%H:%M'):
    #return value.strftime(format)
    return value.ctime()


