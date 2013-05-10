__author__ = 'aparup'
from boilerplate import models
from src.joinhour.models.event import Event
from src.joinhour.models.user_activity import UserActivity


from boilerplate.lib.basehandler import BaseHandler, user_required

class MyCornerHandler(BaseHandler):

    @user_required
    def get(self):
        params = {}
        action = self.request.get('action')
        user_info = models.User.get_by_id(long(self.user_id))
        if "my_activities" == action:
            my_activities = Event.query(Event.username == user_info.username,
                                             Event.type == Event.EVENT_TYPE_ACTIVITY,Event.status != Event.EXPIRED).fetch()
            self.view.events = my_activities
        elif "my_interests" == action:
            my_interests = Event.query(Event.username == user_info.username,
                                             Event.type == Event.EVENT_TYPE_INTEREST,Event.status != Event.EXPIRED).fetch()
            self.view.events = my_interests
        elif "joined_activities" == action:
            joined_activities = UserActivity.query(UserActivity.user == user_info.key,
                                                   UserActivity.status == UserActivity.ACTIVE).fetch()
            self.view.events = joined_activities
        return self.render_template('live_board.html', **params)

