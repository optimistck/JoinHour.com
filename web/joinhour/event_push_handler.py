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

class EventPushHandler(BaseHandler):
    def get(self):
        last_push_record = LastPush.query().get()
        if not last_push_record:
            last_push_record = LastPush()
            events = Event.query().fetch()
        else:
            last_push_date = last_push_record.last_push
            events = Event.query_all_events_since(last_push_date)
        #Send to all users logged in?
        client = memcache.Client()
        key = 'loggedin'
        logged_in_users = client.gets(key)

        for user in logged_in_users:
            for event in events:
                #filter by building
                #render a page for each event, indicating "add/update"
                template = 'some rendered template'
            channel.send_message(user.username, template)

        last_push_record.last_push = datetime.utcnow()
        last_push_record.put()