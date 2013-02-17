# -*- coding: utf-8 -*-

"""
    This is a Stat handler.

    Routes are setup in routes.py and added in main.py
"""
#import httpagentparser

from boilerplate import models
from boilerplate.lib.basehandler import BaseHandler
from boilerplate.lib.basehandler import user_required


# standard library imports
import logging
import random
import re
import json

# related third party imports
import webapp2
import httpagentparser
from webapp2_extras import security
from webapp2_extras.auth import InvalidAuthIdError, InvalidPasswordError
from webapp2_extras.i18n import gettext as _
from webapp2_extras.appengine.auth.models import Unique
from google.appengine.api import taskqueue
from google.appengine.api import users
from github import github
from linkedin import linkedin

# local application/library specific imports
import boilerplate.models
import boilerplate.forms as forms
from boilerplate.lib import utils, captcha, twitter
from boilerplate.lib.basehandler import BaseHandler
from boilerplate.lib.basehandler import user_required
from boilerplate.lib import facebook


# TODO: create and import (here) own models and BaseHandler
from web import stat_models #for now using stat_models. Eventually we'll pull models into the web code, but need to think about the Boilerplate updates too

#JH experimental

import cgi
import datetime
import urllib
import webapp2
from google.appengine.ext import db
from google.appengine.api import users

class TipHandler(BaseHandler):
    """
    Handler for Tip (rating activity participants)
    """

    def get(self):
        """ Returns a simple HTML (for now) for handling tips form """
        params = {}
        return self.render_template('tip.html', **params)



class TestHandler(BaseHandler):
    """
    Handler for a test page to experiment with
    """

    def get(self):
        """ Returns a simple HTML for contact form """
        #TODO: fix.
        if self.user:
            user_info = models.User.get_by_id(long(self.user_id))
            if user_info.name or user_info.last_name:
                self.form.name.data = user_info.name + " " + user_info.last_name
            if user_info.email:
                self.form.email.data = user_info.email
        params = {
            "exception" : self.request.get('exception')
            }

        return self.render_template('test.html', **params)

    def post(self):
        """    Add a quote to the system.    """
        if not self.form.validate():
            return self.get()
        #user = users.get_current_user()
        activity_status = self.form.activity_status.data.strip()
        
        #quote_id = models.add_quote(text, user, uri=uri)
        quote_id = stat_models.add_activity(message)
        self.redirect('/tip/')
        #self.response.out.write(template.render(template_file, template_values))        

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