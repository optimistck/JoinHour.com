from boilerplate.handlers import RegisterBaseHandler
from boilerplate import models
import jinja2


from src.joinhour.models.activity import Activity
from src.joinhour.activity_manager import ActivityManager
from src.joinhour.interest_manager import InterestManager
from src.joinhour.models.interest import Interest
from google.appengine.ext import ndb
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


class HomeRequestHandler(RegisterBaseHandler):
    """
    Handler to show the home page
    """

    def get(self):
        params = {}
        if not self.user:
            return self.render_template('home.html', **params)
        action = str(self.request.get('action'))
        if action == 'delete':
            key = self.request.get('key')
            ndb.Key(urlsafe=key).delete()
        user_info = models.User.get_by_id(long(self.user_id))
        self.view.activities = Activity.query(Activity.username == user_info.username).fetch()
        self.view.interests = Interest.query(Interest.username == user_info.username).fetch()

        return self.render_template('home.html', **params)