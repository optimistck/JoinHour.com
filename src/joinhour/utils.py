import logging
from src.joinhour.models.feedback import UserFeedback
from src.joinhour.models.match import Match

__author__ = 'aparbane'
from UserString import MutableString
from src.joinhour.models.event import Event


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


def hasAvatar(username):
    user = models.User.get_by_username(username)
    if user is None:
        logging.info('user is none')
        return False;
    if user.avatar is not  None:
        return True
    return False

def dateformat(value,format='%H:%M'):
    #return value.strftime(format)
    return value.ctime()

def get_matching_activities(interest_key):
    return Match.query(Match.interest == interest_key).fetch()


def event_attributes(event_key, username):
    event_attributes = {}
    event_manager = EventManager.get(event_key)
    event = event_manager.get_event()
    user = models.User.get_by_username(username)
    type = event.type
    expiration = event_manager.expires_in()
    event_attributes['expiration'] = expiration
    status = event.status
    if type == Event.EVENT_TYPE_SPECIFIC_INTEREST:
        can_join = event_manager.can_join(user.key.id())[0]
        can_leave = event_manager.can_leave(user.key.id())[0]
        if can_join:
            event_attributes['can_join'] = True
        elif can_leave:
            event_attributes['can_leave'] = True
        if status == Event.COMPLETE:
            event_attributes['status'] = 'COMPLETE'
        elif status == Event.INITIATED:
            if expiration != 'EXPIRED':
                event_attributes['status'] = 'CREATED'
        elif status == Event.EXPIRED:
            event_attributes['status'] = 'CLOSED'
        elif status == Event.FORMING:
            if expiration != 'EXPIRED':
                event_attributes['status'] = 'FORMING'
        else:
            event_attributes['status'] = 'CLOSED'
        feedback = UserFeedback.query(UserFeedback.user == user.key,UserFeedback.status == UserFeedback.OPEN,UserFeedback.activity == event.key).fetch()
        if len(feedback) > 0:
            event_attributes['has_feedback'] = True
            event_attributes['feedback'] = feedback[0]
    else:
        if status == Event.INITIATED:
            if expiration == 'EXPIRED':
                event_attributes['status'] = 'CLOSED'
                event_attributes['can_convert'] = False
            else:
                event_attributes['status'] = 'CREATED'
                event_attributes['can_convert'] = True
        elif status == Event.COMPLETE_CONVERTED:
            event_attributes['status'] = 'COMPLETE_CONVERTED'
    return event_attributes


