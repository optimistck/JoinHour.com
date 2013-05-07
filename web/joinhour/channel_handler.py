__author__ = 'ashahab'
import jinja2
from src.joinhour.models.event import Event
from src.joinhour.models.last_push import LastPush
from boilerplate.lib.basehandler import BaseHandler
from src.joinhour.event_manager import EventManager
from google.appengine.api import channel
from  datetime import datetime
from datetime import timedelta
from google.appengine.api import memcache
import os
import logging
from google.appengine.ext import ndb

class ConnectedHandler(BaseHandler):
    def get(self):
        pass
    def post(self):
        client_id = self.request.get('from')
        key = 'loggedin'
        client = memcache.Client()
        while True: # Retry loop
            logged_in_users = client.gets(key)
            if logged_in_users is not none:
                logged_in_users = set()
            logged_in_users.add(client_id)
            if client.cas(key, logged_in_users):
                break
        return self.redirect_to('home')

class DisconnectedHandler(BaseHandler):
    def get(self):
        pass

    def post(self):
        client_id = self.request.get('from')
        key = 'loggedin'
        client = memcache.Client()
        while True: # Retry loop
            logged_in_users = client.gets(key)
            if logged_in_users is not none:
                break;
            logged_in_users.discard(client_id)
            if client.cas(key, logged_in_users):
                break
        return self.redirect_to('home')