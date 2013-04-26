#google imports
import webapp2
from webapp2_extras.i18n import gettext as _
from google.appengine.datastore.datastore_query import Cursor
# Boilerplate imports
from boilerplate.lib.basehandler import BaseHandler, user_required
from boilerplate import models
import jinja2
from  datetime import datetime
from datetime import timedelta

from src.joinhour.models.activity import Activity
from src.joinhour.activity_manager import ActivityManager
from src.joinhour.interest_manager import InterestManager
from src.joinhour.models.interest import Interest
from src.joinhour.utils import *
from google.appengine.ext import ndb


def spots_remaining(key):
    return ActivityManager.get(key).spots_remaining()


jinja2.filters.FILTERS['minute_format'] = minute_format
jinja2.filters.FILTERS['expires_in'] = get_expiration_duration
jinja2.filters.FILTERS['spots_remaining'] = spots_remaining
jinja2.filters.FILTERS['can_join'] = can_join


class ActivityHandler(BaseHandler):
    """
    Handler for the Activity view, formerly the Leaderboard showing all active open activities and pasive interest broadcasts
    """
    #orig
    @user_required
    def get(self):
        user_info = models.User.get_by_id(long(self.user_id))
        building_name = user_info.building
        cursorString = str(self.request.get('cursor'))
        curs = ndb.Cursor(urlsafe=cursorString.lstrip('Cursor(').rstrip(')'))
        q = Activity.query( Activity.building_name == building_name).order(-Activity.date_entered, Activity.key)
        count = 1
        filtered_not_joinable_activities = []
        filtered_joinable_activities = []
        q_iter = q.iter(produce_cursors=True, start_cursor= curs)
        for activity in q_iter:
            if count > 5:
                break
            if activity.username != user_info.username:
                if ActivityManager.get(activity.key.urlsafe()).can_join(self.user_id)[0]:
                    filtered_joinable_activities.append(activity)
                else:
                    filtered_not_joinable_activities.append(activity)
                count += 1
        self.view.activities = filtered_joinable_activities
        self.view.not_joinable_activities = filtered_not_joinable_activities
        self.view.interests = [interest for interest in
                               Interest.get_active_interests_by_building_not_mine(building_name, user_info.username) if
                               InterestManager.get(interest.key.urlsafe()).expires_in() != Interest.EXPIRED]
        params = {'user_id': self.user_id}
        if q_iter.has_next():
            params = {'cursor': q_iter.cursor_after(),
                      'exception': self.request.get('exception'),
                      'user_id': self.user_id
            }
        return self.render_template('stat.html', **params)

    def post(self):
        is_delete = self.request.POST.get('delete_item')
        is_save = self.request.POST.get('save_item')
        if is_delete:
            message = _('You clicked: Details - the go to page is right, the data pull not wired')
            entity_key = _('You clicked Details in the entity_key')
        elif is_save:
            message = _('You clicked: JOIN - this needs to be wired')
            entity_key = _('You clicked JOIN in the entity_key')
        else:
            raise Exception('no form action given')

        self.add_entity_key_to_pass(entity_key)
        self.add_message(message, 'success')
        return self.redirect_to('activity')


    @webapp2.cached_property
    def form(self):
        return forms.StatForm(self)

