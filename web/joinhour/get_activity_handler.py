#google imports
import webapp2
from google.appengine.ext import ndb

# Boilerplate imports
from boilerplate.lib.basehandler import BaseHandler, user_required
from src.joinhour.utils import *
import jinja2

jinja2.filters.FILTERS['expires_in'] = get_expiration_duration
jinja2.filters.FILTERS['minute_format'] = minute_format

class GetActivityHandler(BaseHandler):
    """
    Handler for the Activity view, formerly the Leaderboard showing all active open activities and pasive interest broadcasts
    """

    @user_required
    def get(self):
        ID = self.request.get('ID')
        if ID:
            event = ndb.Key(urlsafe=ID).get()
            self.view.event = event
            event_attributes_list = dict()
            event_attribute = event_attributes(event.key.urlsafe(),self.username)
            event_attributes_list[event.key.urlsafe()] = event_attribute
            self.view.event_attributes_list = event_attributes_list
        params = {}
        return self.render_template('activity_detail.html', **params)

    @webapp2.cached_property
    def form(self):
        return forms.StatForm(self)