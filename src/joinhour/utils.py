__author__ = 'aparbane'

from src.joinhour.activity_manager import ActivityManager
from src.joinhour.interest_manager import InterestManager
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
    if entity_type == 'Activity':
        return ActivityManager.get(key).expires_in()
    else:
        return InterestManager.get(key).expires_in()

