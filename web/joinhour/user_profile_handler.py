from boilerplate import models
from boilerplate.lib.basehandler import BaseHandler, user_required
from src.joinhour.social_media import twitter

__author__ = 'aparbane'


class UserProfileHandler(BaseHandler):

    @user_required
    def get(self):
        username = self.request.get('username')
        params = {}
        if username is not None:
            user = models.User.get_by_username(username)
            self.view.user = user
            if user.twitter_screen_name is not None:
                twitter_data = twitter.get_friends_and_followers_count(user.twitter_screen_name)
                self.view.twitter_friends_count = twitter_data['friends_count']
                self.view.twitter_followers_count = twitter_data['followers_count']
        return self.render_template('user_profile.html', **params)

