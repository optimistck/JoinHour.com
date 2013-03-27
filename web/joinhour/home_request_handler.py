from boilerplate.handlers import RegisterBaseHandler
from boilerplate import models
import jinja2


from src.joinhour.models.activity import Activity
from src.joinhour.activity_manager import ActivityManager
from src.joinhour.interest_manager import InterestManager
from src.joinhour.models.interest import Interest
from google.appengine.ext import ndb
from src.joinhour.models.match import Match
from src.joinhour.models.user_activity import UserActivity
from google.appengine.api import taskqueue


def minute_format(value):
    if value != Activity.EXPIRED and value != Interest.EXPIRED:
        total_seconds = int(value.total_seconds())
        hours, remainder = divmod(total_seconds,60*60)
        minutes, seconds = divmod(remainder,60)
        if hours > 0:
            return str(hours) + ' hours ' + str(minutes) + ' minutes'
        else:
            return str(minutes) + ' minutes'
    return value


def expires_in(key,entity_type):
    if entity_type == 'Activity':
        return ActivityManager.get(key).expires_in()
    else:
        return InterestManager.get(key).expires_in()




def spots_remaining(key):
    return ActivityManager.get(key).spots_remaining()



def get_matching_activity_key(interest_key):
    return Match.query(Match.interest == interest_key).get().activity.urlsafe()

jinja2.filters.FILTERS['minute_format'] = minute_format
jinja2.filters.FILTERS['expires_in'] = expires_in
jinja2.filters.FILTERS['spots_remaining'] = spots_remaining
jinja2.filters.FILTERS['get_matching_activity_key'] = get_matching_activity_key

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
        activities_from_db = Activity.query(Activity.username == user_info.username).fetch()
        self.view.activities = activities_from_db
        self.view.interests = Interest.query(Interest.username == user_info.username).fetch()
        self.view.past_activities = [activity for activity in activities_from_db if activity.status == Activity.COMPLETE]
        self.view.joined_activities = UserActivity.query(UserActivity.user == user_info.key).fetch()
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
        email_url = self.uri_for('taskqueue-send-email')
        template_val = {
            "app_name": self.app.config.get('app_name'),
            "activity_name": category,
            "activity_owner_name": activity_owner_name,
            "participant_username":participant.name+' '+participant.last_name,
            "reason_for_cancellation":reason_for_cancellation
        }
        body = self.jinja2.render_template('emails/activity_cancel_notification_for_participant.txt', **template_val)
        taskqueue.add(url = email_url,params={
            'to':participant.email,
            'subject' : '[JoinHour.com]Activity cancellation notification',
            'body' : body
        })


