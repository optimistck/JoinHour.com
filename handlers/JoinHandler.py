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
from models.Activity import Activity
from models import User as UserModel

#JH experimental

import cgi
import datetime
import urllib
import webapp2
from google.appengine.ext import ndb
from google.appengine.api import users

class JoinHandler(BaseHandler):
    """
    Handler for JoinHandler Form
    """

    #TODO: load the categories and sub-categories from the pull-down menu
    def get(self):
        params = {}
        return self.render_template('join.html', **params)

    def post(self):
        #TODO: the building name needs to come from the user profile
        building_name = 'building_name'

        if self.user:
            user_info = UserModel.User.get_by_id(long(self.user_id))        
            activity = Activity(parent=ndb.Key("ActivityKey", building_name),
                            category = self.form.category.data.strip(),
                            min_number_of_people_to_join = self.form.min_number_of_people_to_join.data.strip(),
                            max_number_of_people_to_join = self.form.max_number_of_people_to_join.data.strip(),
                            duration = self.form.duration.data.strip(),
                            expiration = self.form.expiration.data.strip(),
                            note = self.form.note.data.strip(),
                            username = user_info.username,
                            ip = self.request.remote_addr
                            )
            activity.put()

            message = _("Your interest was registered successfully. We are searching for a match ... ")
            self.add_message(message, 'success')
            return self.redirect_to('stat')

    @webapp2.cached_property
    def form(self):
        return forms.JoinForm(self)