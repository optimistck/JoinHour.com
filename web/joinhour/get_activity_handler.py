#google imports
import webapp2
from google.appengine.ext import ndb

# Boilerplate imports
from boilerplate.lib.basehandler import BaseHandler
from src.joinhour.activity_manager import ActivityManager
from src.joinhour.interest_manager import InterestManager
import jinja2
from  datetime import datetime
from datetime import timedelta

def expires_in(key,entity_type):
    if entity_type == 'Activity':
        return ActivityManager.get(key).expires_in()
    else:
        return InterestManager.get(key).expires_in()

jinja2.filters.FILTERS['expires_in'] = expires_in

#JH experimental

def format_datetime(value, format='medium'):
    return datetime.datetime.strptime(value, '%M').strftime('%M')

jinja2.filters.FILTERS['format_datetime'] = format_datetime

class GetActivityHandler(BaseHandler):
    """
    Handler for the Activity view, formerly the Leaderboard showing all active open activities and pasive interest broadcasts
    """
    #orig
    def get(self):
        #JH: this needs to be dynamic
        ID = self.request.get('ID')
        if (not ID):
          return self.response.out.write("<html><body><h1>You do not belong here</h1></body></html>")
        self.view.a = ndb.Key(urlsafe=ID).get()
        params = {}
        return self.render_template('activity_detail.html', **params)

    @webapp2.cached_property
    def form(self):
        return forms.StatForm(self)