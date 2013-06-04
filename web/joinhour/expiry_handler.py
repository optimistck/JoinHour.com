__author__ = 'ashahab'
from src.joinhour.models.event import Event
from boilerplate.lib.basehandler import BaseHandler
from src.joinhour.event_manager import EventManager


class ExpiryHandler(BaseHandler):

    def get(self):
        events = Event.query_all_active_events()
        for event in events:
            if EventManager.get(event.key.urlsafe()).expires_in() == Event.EXPIRED:
                event.status = Event.EXPIRED
                event.put()

