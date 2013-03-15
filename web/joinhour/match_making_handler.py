__author__ = 'aparbane'

#google imports
from google.appengine.ext import ndb

# Boilerplate imports
from boilerplate.lib.basehandler import BaseHandler
from boilerplate.lib import utils
from src.joinhour.models.interest import Interest
from src.joinhour.models.activity import Activity
from src.joinhour.matchmaker import MatchMaker


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
                self.full_match()
            elif self.request.get('interest') != '':
                interest = self.request.get('interest')
                self.single_match(self.request.get('interest'))
        except Exception , e:
            print e

    def full_match(self):
        """
        Calls MatchMaker to do full match between current set of valid interests and activities.
        First groups the activities and interests into categories and then executes matchmaking. This is done to optimize the time complexity
        At the end of matchmaking pushes the result to notification queue.
        """
        match_list = {}
        for category in self._get_categories():
            if category[0] == '':
                continue
            interest_list = Interest.get_active_interests_by_category(category[0])
            activity_list = Activity.get_active_activities_by_category(category[0])
            match_list = MatchMaker.match_interests_with_activities(interest_list,activity_list,match_list)
        self._process_notification(match_list)

    def single_match(self,interest):
        """
        Calls MatchMaker to do match between a single interest and the set of valid activities.
        At the end of matchmaking pushes the result to notification queue.
        """
        match_list = {}
        activity_list = Activity.get_active_activities_by_category(interest.category)
        match_list = MatchMaker.match_interests_with_activities([ndb.Key(urlsafe=interest).get()], activity_list, match_list)
        self._process_notification(match_list)

    def _get_categories(self):
        return utils.CATEGORY

    def _process_notification(self,match_list):
        pass


