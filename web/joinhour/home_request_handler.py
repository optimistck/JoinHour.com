import jinja2
from google.appengine.ext import ndb
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

def status_filter(status):
    if status == Event.INITIATED:
        return "Looking for a match"
jinja2.filters.FILTERS['minute_format'] = minute_format
jinja2.filters.FILTERS['expires_in'] = get_expiration_duration
jinja2.filters.FILTERS['spots_remaining'] = spots_remaining
jinja2.filters.FILTERS['get_matching_activity_key'] = get_matching_activity_key
jinja2.filters.FILTERS['status_filter'] = status_filter

class HomeRequestHandler(RegisterBaseHandler):
    """
    Handler to show the home page
    """

    def get(self):
        params = {}
        if not self.user:
            return self.render_template('home.html', **params)
        action = str(self.request.get('action'))
        if action == 'delete':
            self._delete_entity(self.request.get('key'))
        elif action == 'cancel':
            category, activity_username,participants = self._cancel_activity(self.request.get('key'))
            activity_user = models.User.get_by_username(activity_username)
            activity_owner_name = activity_user.name + ' ' + activity_user.last_name
            for participant in participants:
                self._push_notification(category,activity_owner_name,participant,self.request.get('reason'))

        user_info = models.User.get_by_id(long(self.user_id))
        activities_from_db = Event.query(Event.username == user_info.username,Event.type == Event.EVENT_TYPE_ACTIVITY).fetch()
        self.view.activities = [activity for activity in activities_from_db if activity.status != Event.EXPIRED]
        self.view.interests = Event.query(Event.username == user_info.username,Event.status != Event.EXPIRED, Event.type == Event.EVENT_TYPE_INTEREST).fetch()
        self.view.joined_activities = UserActivity.query(UserActivity.user == user_info.key).fetch()
        self.view.user_feedbacks = UserFeedback.query(UserFeedback.user == user_info.key,UserFeedback.status == UserFeedback.OPEN).fetch()
        token = channel.create_channel(user_info.username)
        params['token'] = token
        return self.render_template('home.html', **params)

    def _delete_entity(self,key):
        key = self.request.get('key')
        ndb.Key(urlsafe=key).delete()


    def _cancel_activity(self,key):
        activity = ndb.Key(urlsafe=key).get()
        category = activity.category
        activity_username = activity.username
        participants_list = UserActivity.query(UserActivity.activity == activity.key).fetch()
        participants = []
        for participant in participants_list:
            participants.append(participant.user.get())
            participant.key.delete()
        ndb.Key(urlsafe=key).delete()
        return category,activity_username,participants

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


