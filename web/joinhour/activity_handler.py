#google imports
import webapp2
# Boilerplate imports
from boilerplate.lib.basehandler import BaseHandler, user_required
from boilerplate import models
import jinja2

from src.joinhour.models.event import Event
from src.joinhour.event_manager import EventManager
from src.joinhour.utils import *


def spots_remaining(key):
    return EventManager.get(key).spots_remaining()


jinja2.filters.FILTERS['minute_format'] = minute_format
jinja2.filters.FILTERS['expires_in'] = get_expiration_duration
jinja2.filters.FILTERS['spots_remaining'] = spots_remaining
jinja2.filters.FILTERS['can_join'] = can_join
jinja2.filters.FILTERS['count_participants'] = count_participants
jinja2.filters.FILTERS['dateformat'] = dateformat

class ActivityHandler(BaseHandler):
    """
    Handler for the Activity view, formerly the Leaderboard showing all active open activities and pasive interest broadcasts
    """
    @user_required
    def get(self):
        user_info = models.User.get_by_id(long(self.user_id))
        building_name = user_info.building
        self.view.events = Event.query(Event.building_name == building_name).order(-Event.date_entered)
        self.view.building = building_name
        '''
        TODO - For Abin to Implement Pagination
        cursorString = str(self.request.get('cursor'))
        curs = ndb.Cursor(urlsafe=cursorString.lstrip('Cursor(').rstrip(')'))
        q = Event.query( Event.building_name == building_name).order(-Event.date_entered, Event.key)
        count = 1
        filtered_not_joinable_activities = []
        filtered_joinable_activities = []
        q_iter = q.iter(produce_cursors=True, start_cursor= curs)
        for activity in q_iter:
            if count > 5:
                break
            if activity.username != user_info.username:
                if EventManager.get(activity.key.urlsafe()).can_join(self.user_id)[0]:
                    filtered_joinable_activities.append(activity)
                else:
                    filtered_not_joinable_activities.append(activity)
                count += 1
        self.view.building = building_name
        self.view.activities = filtered_joinable_activities
        self.view.not_joinable_activities = filtered_not_joinable_activities
        self.view.interests = [interest for interest in
                               Interest.get_active_interests_by_building_not_mine(building_name, user_info.username) if
                               EventManager.get(interest.key.urlsafe()).expires_in() != Event.EXPIRED]



        if q_iter.has_next():
            params = {'cursor': q_iter.cursor_after(),
                      'exception': self.request.get('exception'),
                      'user_id': self.user_id
            }
        '''
        params = {'user_id': self.user_id}
        return self.render_template('stat.html', **params)




    @webapp2.cached_property
    def form(self):
        return forms.StatForm(self)

