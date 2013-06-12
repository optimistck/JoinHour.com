__author__ = 'aparbane'
import logging
from src.joinhour.models.feedback import UserFeedback
from src.joinhour.models.match import Match
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
        can_cancel = event_manager.can_cancel(user.key.id())[0]
        if can_join:
            event_attributes['can_join'] = True
        elif can_leave:
            event_attributes['can_leave'] = True
        elif can_cancel:
            event_attributes['can_cancel'] = True
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
        event_attributes['spots_remaining'] = event_manager.spots_remaining()
    else:
        if status == Event.INITIATED or status == Event.FORMING:
            if expiration == 'EXPIRED':
                event_attributes['status'] = 'CLOSED'
                event_attributes['can_convert'] = False
            else:
                event_attributes['status'] = 'CREATED'
                event_attributes['can_convert'] = True
        elif status == Event.COMPLETE_CONVERTED:
            event_attributes['status'] = 'COMPLETE_CONVERTED'
    return event_attributes


def get_interest_details(interest_key):
    event_manager = EventManager.get(interest_key)
    event = event_manager.get_event()
    interest_user = models.User.get_by_username(event.username)
    interest_details = dict()
    interest_details['category'] = event.category
    interest_details['meeting_place'] = event.meeting_place
    interest_details['location'] = event.activity_location
    interest_details['start_time'] = event.start_time
    interest_details['username'] = event.username
    participants = event_manager.get_all_companions()
    interest_details['participants'] = participants
    all_participants = [interest_user.name + ' ' + interest_user.last_name]
    for participant in participants:
        all_participants.append(str(participant.user.get().name) + ' ' + str(participant.user.get().last_name))
    interest_details['all_participants'] = all_participants





