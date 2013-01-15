# -*- coding: utf-8 -*-

"""
    This is a Stat handler.

    Routes are setup in routes.py and added in main.py
"""
import httpagentparser

from boilerplate import models
from boilerplate.lib.basehandler import BaseHandler
from boilerplate.lib.basehandler import user_required
# TODO: create and import (here) own models and BaseHandler
from web import stat_models #for now using stat_models. Eventually we'll pull models into the web code, but need to think about the Boilerplate updates too


# Stat code:
class InitiateActivityHandler(BaseHandler):
    """
    Handler for Initiate Activity Form
    """

    def get(self):
        """ Returns a simple HTML (for now) for Activity form """
        params = {}
        return self.render_template('initiate_activity.html', **params)


class AnnouncePassiveInterestHandler(BaseHandler):
    """
    Handler for Announce Passive Interest Form
    """

    def get(self):
        """ Returns a simple HTML (for now) for Passive Interest form """
        params = {}
        return self.render_template('announce_passive_interest.html', **params)

class ActivityDetailHandler(BaseHandler):
    """
    Handler for Activity Detail (shows detail when a user clicks on an activity in the Stat view)
    """

    def get(self):
        """ Returns a simple HTML (for now) for Activity Detail form """
        params = {}
        return self.render_template('activity_detail.html', **params)

class FeedbackHandler(BaseHandler):
    """
    Handler for Feedback (rating activity participants)
    """

    def get(self):
        """ Returns a simple HTML (for now) for Activity Detail form """
        params = {}
        return self.render_template('feedback.html', **params)

class TipHandler(BaseHandler):
    """
    Handler for Tip (rating activity participants)
    """

    def get(self):
        """ Returns a simple HTML (for now) for handling tips form """
        params = {}
        return self.render_template('tip.html', **params)

class StatHandler(BaseHandler):
    """
    Handler for the Stat view, formerly the Leaderboard showing all active open activities and pasive interest broadcasts
    """

    def get(self):
        """ Returns a simple HTML (for now) for handling stat view """
        params = {}
        return self.render_template('stat.html', **params)


### end of stat code

# BP code
class SecureRequestHandler(BaseHandler):
    """
    Only accessible to users that are logged in
    """

    @user_required
    def get(self, **kwargs):
        user_session = self.user
        user_session_object = self.auth.store.get_session(self.request)

        user_info = models.User.get_by_id(long( self.user_id ))
        user_info_object = self.auth.store.user_model.get_by_auth_token(
            user_session['user_id'], user_session['token'])

        try:
            params = {
                "user_session" : user_session,
                "user_session_object" : user_session_object,
                "user_info" : user_info,
                "user_info_object" : user_info_object,
                "userinfo_logout-url" : self.auth_config['logout_url'],
                }
            return self.render_template('secure_zone.html', **params)
        except (AttributeError, KeyError), e:
            return "Secure zone error:" + " %s." % e