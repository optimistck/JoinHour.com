__author__ = 'aparbane'

#google imports
from google.appengine.ext import ndb

# Boilerplate imports
from boilerplate.lib.basehandler import BaseHandler
from boilerplate.lib import utils
from src.joinhour.models.interest import Interest
from src.joinhour.models.activity import Activity
from src.joinhour.matchmaker import MatchMaker
from boilerplate import models
from google.appengine.api import taskqueue


class MatchMakingHandler(BaseHandler):
    """
    Handles the matching making requests.
    If the request has an interest in parameter single_match() for the interested is executed.
    If the request has an activity in parameter full_match() is executed.
    At the end of matchmaking pushes the result to notification queue.
    """
    def get(self):
        try:
            if self.request.get('activity') != '':
                self.match_activity_to_interests(self.request.get('activity'))
            elif self.request.get('interest') != '':
                interest = self.request.get('interest')
                self.match_interest_to_activities(self.request.get('interest'))
            else:
                self.full_match()
        except Exception , e:
            print e

    def full_match(self):
        """
        Calls MatchMaker to do full match between current set of valid interests and activities.
        First groups the activities and interests into categories and then executes matchmaking. This is done to optimize the time complexity
        At the end of matchmaking pushes the result to notification queue.
        """
        match_result_list = {}
        for category in self._get_categories():
            if category[0] == '':
                continue
            interest_list = Interest.get_active_interests_by_category(category[0])
            activity_list = Activity.get_active_activities_by_category(category[0])
            match_result_list = MatchMaker.match_interests_with_activities(interest_list,activity_list,match_result_list)
        self._process_notification(match_result_list)

    def match_interest_to_activities(self,interest_key):
        """
        Calls MatchMaker to do match between a single interest and the set of valid activities.
        At the end of matchmaking pushes the result to notification queue.
        """
        interest = ndb.Key(urlsafe=interest_key).get()
        activity_list = Activity.get_active_activities_by_category_and_building(interest.category,interest.building_name)
        match_list = MatchMaker.match_interests_with_activities([interest], activity_list,{})
        self._process_notification(match_list)

    def match_activity_to_interests(self,activity_key):
        activity = ndb.Key(urlsafe=activity_key).get()
        interest_list = Interest.get_active_interests_by_category_and_building(activity.category, activity.building_name);
        match_list = MatchMaker.match_interests_with_activities(interest_list, [activity],{})
        self._process_notification(match_list)

    def _get_categories(self):
        return utils.CATEGORY

    def _process_notification(self,match_list):
        for user in match_list:
            self._notify_interest_owner(user,match_list[user])

    def _notify_interest_owner(self,username,matches):
        user = models.User.get_by_username(username)

        email_url = self.uri_for('taskqueue-send-email')
        template_val = {
            "app_name": self.app.config.get('app_name'),
            "interest_creator_username": username,
            "matches": matches,
        }
        body = self.jinja2.render_template('emails/match_found_notification_for_interest_owner.txt', **template_val)
        taskqueue.add(url = email_url,params={
            'to':user.email,
            'subject' : '[JoinHour.com]Match notification',
            'body' : body
        })




