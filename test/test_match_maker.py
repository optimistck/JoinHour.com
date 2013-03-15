from src.joinhour.models.activity import Activity
from src.joinhour.models.interest import Interest

__author__ = 'aparbane'

import unittest
from google.appengine.ext import testbed
from src.joinhour.matchmaker import MatchMaker
from src.joinhour.activity_manager import ActivityManager
from src.joinhour.interest_manager import InterestManager



class MatchMakerTest(unittest.TestCase):

    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_taskqueue_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_match_making(self):
        interest_list = []
        activity_list = []
        interest_list.append(InterestManager.create_interest(category='Go for a run',duration='40',expiration='180',username='testuser1',building_name='building_name'))
        interest_list.append(InterestManager.create_interest(category='Go for a run',duration='40',expiration='180',username='testuser2',building_name='building_name'))
        interest_list.append(InterestManager.create_interest(category='Go for a run',duration='20',expiration='180',username='testuser1',building_name='building_name'))
        activity_list.append(ActivityManager.create_activity(category='Go for a run',duration='40',expiration='180',username='testuser',
                                                              building_name ='building_name',ip='127.0.0.1',min_number_of_people_to_join='',max_number_of_people_to_join='',note='meet me at shadyside'))
        activity_list.append(ActivityManager.create_activity(category='Play pool',duration='40',expiration='180',username='testuser',
                                                             building_name='building_name',ip='127.0.0.1',min_number_of_people_to_join='',max_number_of_people_to_join='',note='meet me at shadyside'))
        self.assertEqual(3,len(Interest.get_active_interests_by_category('Go for a run')))
        self.assertEqual(1,len(Activity.get_active_activities_by_category('Go for a run')))
        self.assertEqual(1,len(Activity.get_active_activities_by_category('Play pool')))
        match_list = MatchMaker.match_interests_with_activities(interest_list,activity_list)
        self.assertEqual(2,len(match_list))
        self.assertEqual(4,len(match_list['testuser1']))
        self.assertEqual(2,len(match_list['testuser2']))
        self.assertEqual(MatchMaker.CLOSE_MATCH,match_list['testuser2'][0].match_type)
        self.assertEqual(MatchMaker.CATEGORY_MISMATCH,match_list['testuser2'][1].match_type)
        self.assertEqual(MatchMaker.CLOSE_MATCH,match_list['testuser1'][0].match_type)
        self.assertEqual(MatchMaker.CATEGORY_MISMATCH,match_list['testuser1'][1].match_type)
        self.assertEqual(MatchMaker.DURATION_MISMATCH,match_list['testuser1'][2].match_type)
        self.assertEqual(MatchMaker.CATEGORY_MISMATCH,match_list['testuser1'][3].match_type)




if __name__ == '__main__':
    unittest.main()


