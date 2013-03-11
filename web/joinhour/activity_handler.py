#google imports
import webapp2
from google.appengine.ext import ndb
from webapp2_extras.i18n import gettext as _

# Boilerplate imports
from boilerplate.lib.basehandler import BaseHandler
import jinja2


#JH experimental
from src.joinhour.models.activity import Activity
from src.joinhour.activity_manager import ActivityManager
from src.joinhour.models.interest import Interest

def expires_in(activityId):
    return ActivityManager.get(activityId).expires_in()

jinja2.filters.FILTERS['expires_in'] = expires_in




class ActivityHandler(BaseHandler):
    """
    Handler for the Activity view, formerly the Leaderboard showing all active open activities and pasive interest broadcasts
    """
    #orig
    def get(self):
        #JH: this needs to be dynamic
        building_name = 'building_name'

        self.view.activities = Activity.query().fetch(20)
        self.view.interests = Interest.query().fetch(20)
        params = {}
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
        return self.redirect_to('activity_detail')



    @webapp2.cached_property
    def form(self):
        return forms.StatForm(self)

