__author__ = 'ashahab'
import os
import logging

from google.appengine.ext import ndb
from google.appengine.api.taskqueue import Task

from src.joinhour.utils import get_interest_details
from src.joinhour.models.event import Event
from boilerplate.lib.basehandler import BaseHandler
from src.joinhour.event_manager import EventManager
from src.joinhour.notification_manager import NotificationManager


class ActivityLifeCycleHandler(BaseHandler):
    def get(self):
        try:
            activity_key = self.request.get('activity')
            if activity_key != '':
                activity = ndb.Key(urlsafe=activity_key).get()
                if not activity:
                    return
                if activity.status == Event.FORMED_OPEN:
                    activity.status = Event.FORMED_INITIATED
                    activity.put()
                    self._start_post_activity_completion_process(activity)
                    self._send_readyness_notification(activity)

        except Exception, e:
            logging.warn(e)

    def _send_readyness_notification(self, activity):
        notification_manager = NotificationManager.get(self)
        activity_manager = EventManager.get(activity.key.urlsafe())
        interest_details = get_interest_details(activity_manager.get_event().key.urlsafe())
        for participant in activity_manager.get_all_companions():
            template_val = notification_manager.get_base_template()
            template_val['interest'] = interest_details
            template_val['participant_username'] = participant.user.get().username
            notification_manager.push_notification(participant.user.get().email,
                                                    '[JoinHour.com]Your activity is starting!',
                                                    'emails/activity_formed_and_initiated_for_activity_participant.txt',
                                                    **template_val)

    def _start_post_activity_completion_process(self, activity):
        if os.environ.get('ENV_TYPE') is None:
            if os.environ.get('SERVER_SOFTWARE', '').startswith('Development'):
                eta = 120
            else:
                eta = 1800
            task = Task(url='/post_activity_completion/', method='GET',
                        params={'activity_key': activity.key.urlsafe()},
                        countdown=eta)
            task.add('postActivityCompletion')








