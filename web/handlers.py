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



class MainPage(webapp2.RequestHandler):
  def get(self):
    self.response.out.write('<html><body>')
    guestbook_name=self.request.get('guestbook_name')

    # Ancestor Queries, as shown here, are strongly consistent with the High
    # Replication Datastore. Queries that span entity groups are eventually
    # consistent. If we omitted the ancestor from this query there would be a
    # slight chance that greeting that had just been written would not show up
    # in a query.
    greetings = db.GqlQuery("SELECT * "
                            "FROM Greeting "
                            "WHERE ANCESTOR IS :1 "
                            "ORDER BY date DESC LIMIT 10",
                            stat_models.guestbook_key(guestbook_name))

    for greeting in greetings:
      if greeting.author:
        self.response.out.write(
            '<b>%s</b> wrote:' % greeting.author)
      else:
        self.response.out.write('An anonymous person wrote:')
      self.response.out.write('<blockquote>%s</blockquote>' %
                              cgi.escape(greeting.content))
  
    self.response.out.write("""
    <form action="/sign?%s" method="post">
    <div><textarea name="content" rows="3" cols="60"></textarea></div>
    <div><input type="submit" value="Sign Guestbook"></div>
    </form>
    <hr>
    <form>Guestbook name: <input value="%s" name="guestbook_name">
    <input type="submit" value="switch"></form>
    </body>
    </html>""" % (urllib.urlencode({'guestbook_name': guestbook_name}), cgi.escape(guestbook_name)))
    def post(self): 
        pass

class Guestbook(webapp2.RequestHandler):
  def post(self):
    # We set the same parent key on the 'Greeting' to ensure each greeting is in
    # the same entity group. Queries across the single entity group will be
    # consistent. However, the write rate to a single entity group should
    # be limited to ~1/second.
    guestbook_name = self.request.get('guestbook_name')
    greeting = stat_models.Greeting(parent=stat_models.guestbook_key(guestbook_name))

    if users.get_current_user():
      greeting.author = users.get_current_user().nickname()

    greeting.content = self.request.get('content')
    greeting.put()
    self.redirect('/test?' + urllib.urlencode({'guestbook_name': guestbook_name}))

#JH experimental END



# Stat code:
##class InitiateActivityHandler(BaseHandler):
##    """
##    Handler for Initiate Activity Form
##    """

##    def get(self):
##        """ Returns a simple HTML (for now) for Activity form """
##        params = {}
##        return self.render_template('initiate_activity.html', **params)


##class AnnouncePassiveInterestHandler(BaseHandler):
##    """
##    Handler for Announce Passive Interest Form
##    """

##    def get(self):
##        """ Returns a simple HTML (for now) for Passive Interest form """
##        params = {}
##        return self.render_template('announce_passive_interest.html', **params)

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

    #def get(self):
        #""" Returns a simple HTML - for testing only """
        #params = {}
        #return self.render_template('test.html', **params)

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

    ### TODO: remove? Not needed?
    #@webapp2.cached_property
    #def form(self):
        # change to test form?
        #return forms.ContactForm(self)

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