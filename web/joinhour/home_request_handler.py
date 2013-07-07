import jinja2
from google.appengine.api import channel

from boilerplate.handlers import RegisterBaseHandler
from boilerplate import models
from src.joinhour.event_manager import EventManager
from src.joinhour.notification_manager import NotificationManager
from src.joinhour.models.match import Match
from src.joinhour.models.user_activity import UserActivity
from src.joinhour.models.feedback import UserFeedback
from src.joinhour.utils import *


def spots_remaining(key):
    return EventManager.get(key).spots_remaining()



def get_matching_activity_key(interest_key):
    return Match.query(Match.interest == interest_key).get().activity.urlsafe()

def isValidUser(user_id):
    user_info = models.User.get_by_id(long(user_id))
    if user_info is not None and user_info.building is not None:
        return True
    return False

def status_filter(status):
    if status == Event.INITIATED:
        return "Looking for a match"
jinja2.filters.FILTERS['minute_format'] = minute_format
jinja2.filters.FILTERS['expires_in'] = get_expiration_duration
jinja2.filters.FILTERS['spots_remaining'] = spots_remaining
jinja2.filters.FILTERS['get_matching_activity_key'] = get_matching_activity_key
jinja2.filters.FILTERS['status_filter'] = status_filter
jinja2.filters.FILTERS['isValidUser'] = isValidUser

class HomeRequestHandler(RegisterBaseHandler):
    """
    Handler to show the home page
    """

    def get(self):
        params = {}
        if not self.user:
            return self.render_template('home.html', **params)
        if self.user:
            user_info = models.User.get_by_id(long(self.user_id))
            if user_info.building is None:
                logging.info('no building assigned to user')
                self.redirect_to('complete_profile_social_user')

        action = str(self.request.get('action'))
        if action == 'delete':
            event_manager = EventManager.get(self.request.get('key'))
            event_manager.cancel()
        elif action == 'cancel':
            event_manager = EventManager.get(self.request.get('key'))
            participants = event_manager.get_all_companions()
            category = event_manager.get_event().category
            activity_username = event_manager.get_event().username
            event_manager.cancel()
            activity_user = models.User.get_by_username(activity_username)
            activity_owner_name = activity_user.name + ' ' + activity_user.last_name
            for participant in participants:
                self._push_notification(category,activity_owner_name,participant,self.request.get('reason'))
        user_info = models.User.get_by_id(long(self.user_id))

        my_interests = Event.query(Event.username == user_info.username
                                             ,Event.status != Event.EXPIRED).fetch()
        event_attributes_list = dict()
        for event in my_interests:
            event_attribute = event_attributes(event.key.urlsafe(),self.username)
            event_attributes_list[event.key.urlsafe()] = event_attribute
        self.view.my_interests = my_interests
        self.view.event_attributes_list = event_attributes_list
        token = channel.create_channel(self.user_id)
        params['token'] = token
        return self.render_template('home.html', **params)





    def _push_notification(self,category,activity_owner_name,participant,reason_for_cancellation):

        template_val = {
            "app_name": self.app.config.get('app_name'),
            "activity_name": category,
            "activity_owner_name": activity_owner_name,
            "participant_username": participant.name+' '+participant.last_name,
            "reason_for_cancellation":reason_for_cancellation
        }
        notification_manager = NotificationManager.get()
        notification_manager.push_notification(participant.email,
                                               '[JoinHour.com]Activity cancellation notification',
                                               'emails/activity_cancel_notification_for_participant.txt',
                                               **template_val)


