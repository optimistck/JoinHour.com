#google imports
# Boilerplate imports
import jinja2
from google.appengine.datastore.datastore_query import Cursor

from boilerplate.lib.basehandler import BaseHandler, user_required
from boilerplate import models
from src.joinhour.models.event import Event
from src.joinhour.event_manager import EventManager
from src.joinhour.utils import *


def spots_remaining(key):
    return EventManager.get(key).spots_remaining()

def get_all_companions(key):
    companions = []
    for companion in EventManager.get(key).get_all_companions():
        username = companion.user.get().username
        companions.append('<a href="/user_profile/?username='+username+'">'+username+'</a>')
    return companions


jinja2.filters.FILTERS['minute_format'] = minute_format
jinja2.filters.FILTERS['expires_in'] = get_expiration_duration
jinja2.filters.FILTERS['spots_remaining'] = spots_remaining
jinja2.filters.FILTERS['can_join'] = can_join
jinja2.filters.FILTERS['get_all_companions'] = get_all_companions
jinja2.filters.FILTERS['dateformat'] = dateformat
jinja2.filters.FILTERS['hasAvatar'] = hasAvatar
jinja2.filters.FILTERS['event_attributes'] = event_attributes
jinja2.filters.FILTERS['get_matching_activities'] = get_matching_activities
jinja2.filters.FILTERS['get_request_details'] = get_request_details
jinja2.filters.FILTERS['get_open_requests_for_activity'] = get_open_requests_for_activity
jinja2.filters.FILTERS['get_open_request_for_activity_user'] = get_open_request_for_activity_user
jinja2.filters.FILTERS['get_full_name'] = get_full_name



class ActivityHandler(BaseHandler):
    """
    Handler for the liveboard
    """
    @user_required
    def get(self):
        params = {}
        cursorStr = str(self.request.get('cursor'))
        user_info = models.User.get_by_id(long(self.user_id))
        building_name = user_info.building
        self.view.building = building_name
        cursor = Cursor(urlsafe=cursorStr.lstrip('Cursor(').rstrip(')'))
        events, next_cursor, more = Event.query(Event.building_name == building_name).order(-Event.date_entered).fetch_page(15, start_cursor=cursor)
        event_attributes_list = dict()
        for event in events:
            event_attribute = event_attributes(event.key.urlsafe(),self.username)
            event_attributes_list[event.key.urlsafe()] = event_attribute
        self.view.events = events
        self.view.event_attributes_list = event_attributes_list
        self.view.cursor = next_cursor
        self.view.more = more
        if cursorStr is not None and cursorStr != "":
            return self.render_template('event_list.html', **params)
        else:
            return self.render_template('stat.html', **params)






