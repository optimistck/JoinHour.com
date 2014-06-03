__author__ = 'Constantin Kostenko, Aparup'


from boilerplate.lib.basehandler import BaseHandler
from src.joinhour.models.event import Event
from boilerplate.models import User
from src.joinhour.notification_manager import NotificationManager
import logging


class ActivityDigestHandler(BaseHandler):



    """
    Handles sending the digest of activities to the group members.
    At the end of activity and interest list composition it pushes the result to notification queue.
    """
    def get(self):
        logging.info("Entered the ActivityDigestHandler")
        #TODO Groups should be configured in config file
        groups = ["Test Group","TBD"]
        for group in groups:
            #Get ActiveEvents per group
            events = Event.query_all_active_events_by_building(group)
            #if events:
            if len(events) > 0:
                users = User.get_by_group(group)
                for user in users:
                    self._push_notification(events,user)


    def _push_notification(self, events,user):
        notification_manager = NotificationManager.get(self)
        template_val = notification_manager.get_base_template()
        template_val['recipient'] = user.name
        template_val['events'] = events
        notification_manager.push_notification(user.email,'ActiMom.com: Activity & Interest Digest!','emails/digest_of_activities.txt',**template_val)





