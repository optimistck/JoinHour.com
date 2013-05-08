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
            if not logged_in_users:
                logged_in_users = set()
                logged_in_users.add(client_id)
                client.set(key, logged_in_users)
                break
            else:
                logged_in_users.add(client_id)
                if client.cas(key, logged_in_users):
                    break

class DisconnectedHandler(BaseHandler):
    def get(self):
        pass

    def post(self):
        client_id = self.request.get('from')
        key = 'loggedin'
        client = memcache.Client()
        while True: # Retry loop
            logged_in_users = client.gets(key)
            if not logged_in_users:
                break;
            else:
                logged_in_users.discard(client_id)
                if client.cas(key, logged_in_users):
                    break