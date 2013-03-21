from google.appengine.ext import ndb
from src.joinhour.models.activity import Activity
from src.joinhour.models.interest import Interest

__author__ = 'aparbane'
from datetime import timedelta
from src.joinhour.models.match import Match
from boilerplate.lib import utils
import math


class MatchMaker(object):
    DURATION_TOLERANCE_MINUTES = 10
    TIME_INTERVAL_TOLERANCE_SECONDS = 300


    @classmethod
    def match_interest_with_activities(cls, interest_key):
        """
        Match between An interest and the list of valid activities in the store for a building
        """
        interest = ndb.Key(urlsafe=interest_key).get()
        activity_list = Activity.get_active_activities_by_category_and_building(interest.category,
                                                                                interest.building_name)
        return cls.match_interests_with_activities([interest], activity_list, {})

    @classmethod
    def match_activity_with_interests(cls, activity_key):
        """
        Match between An activity and the list of valid interests in the data store for a building
        """
        activity = ndb.Key(urlsafe=activity_key).get()
        interest_list = Interest.get_active_interests_by_category_and_building(activity.category,
                                                                               activity.building_name);
        return cls.match_interests_with_activities(interest_list, [activity], {})

    @classmethod
    def match_all(cls):
        """
        Match between list of all valid interests and activities in the datastore.
        Match is made in groups of listed categorized by interest and activity category
        """
        match_result_list = {}
        for category in cls._get_categories():
            if category[0] == '':
                continue
            interest_list = Interest.get_active_interests_by_category(category[0])
            activity_list = Activity.get_active_activities_by_category(category[0])
            cls.match_interests_with_activities(interest_list,activity_list,match_result_list)
        return match_result_list


    @classmethod
    def match_interests_with_activities(cls, interest_list, activity_list, match_list={}):
        """
        Tests a list of interests and activities for match.
        Returns a list of Match models , which also gets persisted to datastore
        It is implemented using linear search with isMatch acting as compare function
        It is self sufficient function, and checks for validity of an activity and interest during match.
        :param interest_list: A List of Interests
        :param activity_list: A List of Activities
        :return: A dictionary of the form (username,[Match])
        """
        for interest in interest_list:
            if interest.status == 'EXPIRED' or interest.status == 'COMPLETE':
                continue
            for activity in activity_list:
                #Do we really need this in the core algorithm?
                if activity.username == interest.username:
                    continue
                    #Do we really need this in the core algorithm?
                if activity.building_name != interest.building_name:
                    continue
                if activity.status == 'EXPIRED' or activity.status == 'COMPLETE':
                    continue
                if Match.already_tested_for_match(activity.key, interest.key) is not None:
                    continue
                match_found = cls.isMatch(interest, activity)
                if match_found:
                    interest.status = Interest.COMPLETE
                    interest.put()
                    match = Match(interest=interest.key,
                                  activity=activity.key)
                    match.put()
                    if interest.username in match_list:
                        match_list[interest.username].append(match)
                    else:
                        list = []
                        list.append(match)
                        match_list[interest.username] = list
        return match_list



    @classmethod
    def isMatch(cls, interest, activity):
        if interest.category != activity.category:
            return False
        interest_start_time = interest.date_entered
        interest_expiration_time = interest_start_time + timedelta(minutes=int(str(interest.expiration)))
        interest_duration = interest.duration
        activity_duration = activity.duration
        activity_start_time = activity.date_entered
        activity_expiration_time = activity_start_time + timedelta(minutes=int(str(activity.expiration)))
        if abs((activity_expiration_time - interest_expiration_time).total_seconds()) < cls.TIME_INTERVAL_TOLERANCE_SECONDS:
            if cls._compare_duration(interest_duration, activity_duration):
                return True

    @classmethod
    def _compare_duration(cls, duration1, duration2):
        if math.fabs(int(str(duration1)) - int(str(duration2))) > cls.DURATION_TOLERANCE_MINUTES:
            return False
        return True

    @classmethod
    def _get_categories(self):
        return utils.CATEGORY

























