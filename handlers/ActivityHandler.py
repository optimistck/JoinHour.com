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

class ActivityHandler(BaseHandler):
    """
    Handler for the Activity view, formerly the Leaderboard showing all active open activities and pasive interest broadcasts
    """
    #orig
    def get(self):
        #JH: this needs to be dynamic
        building_name = 'building_name'
        self.view.interests = models.Passive_Interest.query().fetch(20)
        #For active
        ancestor_key = ndb.Key("ActivityKey", building_name)
        self.view.activities = Activity.query_activity(ancestor_key).fetch(20)
        #JH: passing of params is not applicable for the variables with self.view.XXXXX - they get passed right on to .html via {{}}
        params = {}
        return self.render_template('stat.html', **params)
  
    def post(self):
        is_delete = self.request.POST.get('delete_item') 
        is_save = self.request.POST.get('save_item') 
        if is_delete: 
            message = _('You clicked: Details - the go to page is right, the data pull not wired')
            entity_key = _('You clicked Details in the entity_key')
        elif is_save: 
            message = _('You clicked: JOIN - this needs to be wired')
            entity_key = _('You clicked JOIN in the entity_key')
        else: 
            raise Exception('no form action given') 
        
        self.add_entity_key_to_pass(entity_key)
        logging.info('******************')
        logging.info(self.entity_keys)
        self.add_message(message, 'success')
        return self.redirect_to('activity_detail')


    @webapp2.cached_property
    def form(self):
        return forms.StatForm(self)