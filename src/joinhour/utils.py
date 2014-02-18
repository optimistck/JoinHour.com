from  datetime import datetime
from boilerplate.external.pytz import timezone
from boilerplate.external.pytz.reference import Local

__author__ = 'aparbane'
import logging
from src.joinhour.models.feedback import UserFeedback
from src.joinhour.models.match import Match
from src.joinhour.models.event import Event
from src.joinhour.models.request import Request
from src.joinhour.event_manager import EventManager
from src.joinhour.request_manager import RequestManager
from boilerplate import models
from google.appengine.ext import ndb


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

def get_open_requests_for_activity(activity_key):
    return Request.get_open_requests_for_activity(activity_key)

def get_open_request_for_activity_user(activity_key,username):
    user = models.User.get_by_username(username)
    return Request.get_open_request_for_activity_user(activity_key,user.key)

def get_full_name(username):
    user = models.User.get_by_username(username)
    return user.name + " " + user.last_name


def event_attributes(event_key, username):
    event_attributes = {}
    event_manager = EventManager.get(event_key)
    event = event_manager.get_event()
    user = models.User.get_by_username(username)
    type = event.type
    expiration = event_manager.expires_in()
    event_attributes['expiration'] = expiration
    can_join = event_manager.can_join(user.key.id())[0]
    can_leave = event_manager.can_leave(user.key.id())[0]
    can_cancel = event_manager.can_cancel(user.key.id())[0]
    can_initiate_join_request = Request.can_initiate(event_manager.get_event().key,user.key)
    can_cancel_join_request = Request.can_cancel(event_manager.get_event().key,user.key)
    if can_join and can_initiate_join_request:
        event_attributes['can_join'] = True
    if can_cancel_join_request:
        event_attributes['can_cancel_join_request'] = True
    if can_leave:
        event_attributes['can_leave'] = True
    if can_cancel:
        event_attributes['can_cancel'] = True
    if event.start_time is not None:
        start_time = str(event.start_time)
        if start_time.find('.') > 0:
            event_attributes['start_time'] = start_time[0:start_time.find('.')]
        else:
            event_attributes['start_time'] = start_time
    if type == Event.EVENT_TYPE_SPECIFIC_INTEREST:
        feedback = UserFeedback.query(UserFeedback.user == user.key,UserFeedback.status == UserFeedback.OPEN,UserFeedback.activity == event.key).fetch()
        if len(feedback) > 0:
            event_attributes['has_feedback'] = True
            event_attributes['feedback'] = feedback[0]
        event_attributes['spots_remaining'] = event_manager.spots_remaining()
    return event_attributes


def get_interest_details(interest_key):
    event_manager = EventManager.get(interest_key)
    event = event_manager.get_event()
    interest_user = models.User.get_by_username(event.username)
    interest_details = dict()
    interest_details['category'] = event.category
    interest_details['meeting_place'] = event.meeting_place
    interest_details['location'] = event.activity_location
    if event.start_time is not None:
        start_time = event.start_time - datetime.utcnow()
        if start_time.total_seconds() > 0:
            interest_details['start_time'] = minute_format(start_time)
    interest_details['username'] = event.username
    participants = event_manager.get_all_companions()
    interest_details['participants'] = participants
    all_participants = [interest_user.name + ' ' + interest_user.last_name]
    for participant in participants:
        all_participants.append(str(participant.user.get().name) + ' ' + str(participant.user.get().last_name))
    interest_details['all_participants'] = ' , '.join(all_participants)
    return interest_details

def get_request_details(request_key,username):
    request_manager = RequestManager.get(request_key)
    request = request_manager.get_request()
    request_details = dict()
    request_details['requester'] = request.requester.get().username
    request_details['can_accept'] = request_manager.can_accept(username)
    request_details['can_reject'] = request_manager.can_reject(username)
    request_details['can_cancel'] = request_manager.can_cancel(username)
    return request_details





