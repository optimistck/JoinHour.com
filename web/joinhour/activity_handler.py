#google imports
import webapp2
from webapp2_extras.i18n import gettext as _

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



def spots_remaining(key):
    return ActivityManager.get(key).spots_remaining()

jinja2.filters.FILTERS['minute_format'] = minute_format
jinja2.filters.FILTERS['expires_in'] = get_expiration_duration
jinja2.filters.FILTERS['spots_remaining'] = spots_remaining


class ActivityHandler(BaseHandler):
    """
    Handler for the Activity view, formerly the Leaderboard showing all active open activities and pasive interest broadcasts
    """
    #orig
    @user_required
    def get(self):
        user_info = models.User.get_by_id(long(self.user_id))
        building_name = user_info.building
        activities_from_db = Activity.query(Activity.building_name == building_name, Activity.username != user_info.username).fetch()
        self.view.activities = [activity for activity in activities_from_db if ActivityManager.get(activity.key.urlsafe()).can_join(self.user_id)[0]]
        self.view.interests = [interest for interest in Interest.get_active_interests_by_building_not_mine(building_name,user_info.username) if InterestManager.get(interest.key.urlsafe()).expires_in() != Interest.EXPIRED]
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
        return self.redirect_to('activity')



    @webapp2.cached_property
    def form(self):
        return forms.StatForm(self)

