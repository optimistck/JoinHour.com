__author__ = 'aparbane'
from datetime import timedelta
from src.joinhour.models.match import Match
import math



class MatchMaker(object):

    CLOSE_MATCH = 'CLOSE_MATCH'
    APPROX_MATCH = 'APPROX_MATCH'
    TIME_INTERVAL_NO_MATCH = 'TIME_INTERVAL_NO_MATCH'
    DURATION_MISMATCH = 'DURATION_MISMATCH'
    CATEGORY_MISMATCH = 'CATEGORY_MISMATCH'
    DURATION_TOLERANCE_MINUTES = 10
    TIME_INTERVAL_TOLERANCE_SECONDS = 300

    @classmethod
    def match_interests_with_activities(cls,interest_list,activity_list,match_list={}):
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
            if interest.status == 'EXPIRED':
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
                if Match.already_tested_for_match(activity.key,interest.key) is not None:
                    continue
                match_result, match_type = cls.isMatch(interest,activity)
                match = Match(interest=interest.key,
                              activity=activity.key,match_type=match_type)
                match.put()
                if interest.username in match_list:
                    match_list[interest.username].append(match)
                else:
                    list = []
                    list.append(match)
                    match_list[interest.username] = list
        return match_list

    @classmethod
    def isMatch(cls,interest,activity):
        if interest.category != activity.category:
            return False,cls.CATEGORY_MISMATCH
        interest_start_time = interest.date_entered
        interest_expiration_time = interest_start_time + timedelta(minutes= int(str(interest.expiration)))
        interest_duration = interest.duration
        activity_duration = activity.duration
        activity_start_time = activity.date_entered
        activity_expiration_time = activity_start_time + timedelta(minutes= int(str(activity.expiration)))
        if abs((interest_start_time - activity_start_time).total_seconds()) < cls.TIME_INTERVAL_TOLERANCE_SECONDS and abs((interest_expiration_time - activity_expiration_time).total_seconds()) < cls.TIME_INTERVAL_TOLERANCE_SECONDS:
            if cls._compare_duration(interest_duration,activity_duration):
                return True, cls.CLOSE_MATCH
            else:
                return False, cls.DURATION_MISMATCH
        elif interest_start_time < activity_start_time < interest_expiration_time:
            if cls._compare_duration(interest_duration,activity_duration):
                return True, cls.APPROX_MATCH
            else:
                return False, cls.DURATION_MISMATCH
            pass
        elif interest_start_time < activity_expiration_time < interest_expiration_time:
            if cls._compare_duration(interest_duration,activity_duration):
                return True, cls.APPROX_MATCH
            else:
                return False, cls.DURATION_MISMATCH
            pass
        else:
                return False,cls.TIME_INTERVAL_NO_MATCH

    @classmethod
    def _compare_duration(cls,duration1,duration2):
        if math.fabs(int(str(duration1)) - int(str(duration2))) > cls.DURATION_TOLERANCE_MINUTES:
            return False
        return True
























