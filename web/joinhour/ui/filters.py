__author__ = 'aparbane'

from boilerplate.external.pytz import timezone
from boilerplate.external.pytz.reference import Local

def to_local_time_zone(datetime):
    return datetime.astimezone(timezone(Local))