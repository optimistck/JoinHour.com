__author__ = 'ashahab'
import webapp2
from boilerplate.lib.basehandler import BaseHandler
from boilerplate import forms
from src.joinhour.token_generator import TokenGenerator
from webapp2_extras.i18n import gettext as _
from boilerplate.handlers import RegisterBaseHandler
from boilerplate import models
import jinja2


from src.joinhour.models.activity import Activity
from src.joinhour.activity_manager import ActivityManager

class UpdateActivityHandler(BaseHandler):
    """
    Handles the matching making requests.
    At the end of matchmaking pushes the result to notification queue.
    """
    def get(self):
        """ Returns a simple HTML for contact form """

        user_info = models.User.get_by_id(long(self.request.get('user_id')))
        self.view.activities = Activity.query(Activity.username == user_info.username).fetch()

        params = {
            "exception" : self.request.get('exception')
        }
        return self.render_template('activity_list.html', **params)

