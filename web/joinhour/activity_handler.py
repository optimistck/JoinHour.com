#google imports
# Boilerplate imports
import jinja2
from google.appengine.datastore.datastore_query import Cursor

from boilerplate.lib.basehandler import BaseHandler
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
jinja2.filters.FILTERS['display_status'] = display_status

class ActivityHandler(BaseHandler):
    """
    Handler for the Activity view, formerly the Leaderboard showing all active open activities and pasive interest broadcasts
    """
    def get(self):
        params = {}
        cursorStr = str(self.request.get('cursor'))
        user_info = models.User.get_by_id(long(self.user_id))
        building_name = user_info.building
        self.view.building = building_name
        cursor = Cursor(urlsafe=cursorStr.lstrip('Cursor(').rstrip(')'))
        events, next_cursor, more = Event.query(Event.building_name == building_name).order(-Event.date_entered).fetch_page(5, start_cursor=cursor)
        self.view.events = events
        self.view.cursor = next_cursor
        self.view.more = more
        if cursorStr is not None and cursorStr != "":
            return self.render_template('event_list.html', **params)
        else:
            return self.render_template('stat.html', **params)



