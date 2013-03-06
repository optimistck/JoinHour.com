#google imports
import webapp2
from google.appengine.ext import ndb

# Boilerplate imports
from boilerplate.lib.basehandler import BaseHandler
from boilerplate.lib.basehandler import user_required
from src.joinhour.models.activity import Activity



#JH experimental


class GetActivityHandler(BaseHandler):
    """
    Handler for the Activity view, formerly the Leaderboard showing all active open activities and pasive interest broadcasts
    """
    #orig
    def get(self):
        #JH: this needs to be dynamic
        building_name = 'building_name'
        ID = self.request.get('ID')
        if (not ID):
          return self.response.out.write("<html><body><h1>You do not belong here</h1></body></html>")
          
        self.view.a = ndb.Key(urlsafe=ID).get()
        #For active
        ancestor_key = ndb.Key("ActivityKey", building_name)
        self.view.activities = Activity.query_activity(ancestor_key).fetch(20)
        #JH: passing of params is not applicable for the variables with self.view.XXXXX - they get passed right on to .html via {{}}
        params = {}
        return self.render_template('activity_detail.html', **params)

    @webapp2.cached_property
    def form(self):
        return forms.StatForm(self)