from src.joinhour.models.event import Event

__author__ = 'ashahab'
from boilerplate.lib.basehandler import BaseHandler
from boilerplate import models



class NewActivityHandler(BaseHandler):

    def get(self):
        """ Returns a simple HTML for contact form """

        user_info = models.User.get_by_id(long(self.request.get('user_id')))
        self.view.activities = Event.query(Event.username == user_info.username, Event.type == Event.EVENT_TYPE_ACTIVITY).fetch()

        params = {
            "exception" : self.request.get('exception')
        }
        return self.render_template('activity_list.html', **params)