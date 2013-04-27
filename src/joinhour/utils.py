from src.joinhour.models.event import Event

__author__ = 'aparbane'

from src.joinhour.event_manager import EventManager


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

def count_participants(key):
    event_manager = EventManager.get(key)
    if event_manager.get_event().type == Event.EVENT_TYPE_ACTIVITY:
        return len(event_manager.get_all_companions())
    return 0

def dateformat(value,format='%H:%M'):
    #return value.strftime(format)
    return value.ctime()


