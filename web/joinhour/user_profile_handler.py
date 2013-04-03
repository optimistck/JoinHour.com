from boilerplate import models
from boilerplate.lib.basehandler import BaseHandler, user_required

__author__ = 'aparbane'


class UserProfileHandler(BaseHandler):

    @user_required
    def get(self):
        username = self.request.get('username')
        params = {}
        if username is not None:
            user = models.User.get_by_username(username)
            self.view.user = user
        return self.render_template('user_profile.html', **params)

