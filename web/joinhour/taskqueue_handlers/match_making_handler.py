__author__ = 'aparbane'

from urlparse import urlparse

from boilerplate.lib.basehandler import BaseHandler
from src.joinhour.matchmaker import MatchMaker
from boilerplate import models
from src.joinhour.notification_manager import NotificationManager


class MatchMakingHandler(BaseHandler):
    """
    Handles the matching making requests.
    At the end of matchmaking pushes the result to notification queue.
    """
    def get(self):
        try:
            activity_key = self.request.get('activity')
            interest_key = self.request.get('interest')
            match_list = {}
            if activity_key != '':
                match_list = MatchMaker.match_activity_with_interests(activity_key)
            elif interest_key != '':
                match_list = MatchMaker.match_interest_with_activities(interest_key)
            else:
                match_list = MatchMaker.match_all()
            self._process_notification(match_list)
        except Exception , e:
            print e

    def _process_notification(self,match_list):
        #Fire a notification for each user on their channel
        for user in match_list:
            self._notify_interest_owner(user,match_list[user])

    def _notify_interest_owner(self,username,matches):
        user = models.User.get_by_username(username)

        url_object = urlparse(self.request.url)
        if url_object.port is not None:
            url_str = url_object.scheme + '://' + str(url_object.hostname) + ':' +str(url_object.port)
        else:
            url_str = url_object.scheme + '://' + str(url_object.hostname)
        template_val = {
            "app_name": self.app.config.get('app_name'),
            "interest_creator_name": user.name+' '+user.last_name,
            "matches": matches,
            "url" : url_str
        }
        notification_manager = NotificationManager.get()
        notification_manager.push_notification(user.email,
                                               'ActiMom.com: Match notification',
                                               'emails/match_found_notification_for_interest_owner.txt',
                                               **template_val)




