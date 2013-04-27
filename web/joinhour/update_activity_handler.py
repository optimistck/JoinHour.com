__author__ = 'ashahab'
from boilerplate.lib.basehandler import BaseHandler
from boilerplate import models

from src.joinhour.models.activity import Activity


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

