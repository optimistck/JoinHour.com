__author__ = 'aparbane'

from src.joinhour.event_manager import EventManager
from src.joinhour.models.activity import Activity
from src.joinhour.models.interest import Interest


def minute_format(timedelta):
    if timedelta != Activity.EXPIRED and timedelta != Interest.EXPIRED:
        total_seconds = int(timedelta.total_seconds())
        hours, remainder = divmod(total_seconds, 60*60)
        minutes, seconds = divmod(remainder, 60)
        if hours > 0:
            return str(hours) + ' hours ' + str(minutes) + ' minutes'
        else:
            return str(minutes) + ' minutes'
    return timedelta



def get_expiration_duration(key, entity_type):
    return EventManager.get(key).expires_in()

def can_join(key, user_id):
    EventManager.get(key).can_join(user_id)[0]