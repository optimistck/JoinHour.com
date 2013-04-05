__author__ = 'aparbane'

from boilerplate.lib.basehandler import BaseHandler
from src.joinhour.matchmaker import MatchMaker
from boilerplate import models
from google.appengine.api import taskqueue
from urlparse import urlparse


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
        email_url = self.uri_for('taskqueue-send-email')
        url_object = urlparse(self.request.url)
        template_val = {
            "app_name": self.app.config.get('app_name'),
            "interest_creator_name": user.name+' '+user.last_name,
            "matches": matches,
            "url" : url_object.scheme + '://' + str(url_object.hostname) + ':' +str(url_object.port)
        }
        body = self.jinja2.render_template('emails/match_found_notification_for_interest_owner.txt', **template_val)
        taskqueue.add(url = email_url,params={
            'to': user.email,
            'subject' : '[JoinHour.com]Match notification',
            'body' : body
        })




