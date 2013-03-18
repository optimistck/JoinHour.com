#google imports
import webapp2
from webapp2_extras.i18n import gettext as _

# Boilerplate imports
from boilerplate.lib.basehandler import BaseHandler
from boilerplate import models
import jinja2
from  datetime import datetime
from datetime import timedelta

from src.joinhour.models.activity import Activity
from src.joinhour.activity_manager import ActivityManager
from src.joinhour.interest_manager import InterestManager
from src.joinhour.models.interest import Interest
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

jinja2.filters.FILTERS['minute_format'] = minute_format


def expires_in(key,entity_type):
    if entity_type == 'Activity':
        return ActivityManager.get(key).expires_in()
    else:
        return InterestManager.get(key).expires_in()

jinja2.filters.FILTERS['expires_in'] = expires_in


def spots_remaining(key):
    return ActivityManager.get(key).spots_remaining()

jinja2.filters.FILTERS['spots_remaining'] = spots_remaining


class ActivityHandler(BaseHandler):
    """
    Handler for the Activity view, formerly the Leaderboard showing all active open activities and pasive interest broadcasts
    """
    #orig
    def get(self):
        if not self.user:
            return self.redirect_to('login')
        user_info = models.User.get_by_id(long(self.user_id))
        building_name = user_info.building
        activities_from_db = Activity.query(Activity.building_name == building_name, Activity.username != user_info.username).fetch()
        self.view.activities = [activity for activity in activities_from_db if ActivityManager.get(activity.key.urlsafe()).can_join(self.user_id)[0]]
        self.view.interests = Interest.query(Interest.building_name == building_name,Interest.username != user_info.username).fetch()
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

