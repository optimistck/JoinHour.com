

__author__ = 'aparbane'

import unittest
from google.appengine.ext import testbed
from src.joinhour.matchmaker import MatchMaker
from src.joinhour.event_manager import EventManager
from src.joinhour.models.event import Event



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
        #Create some interests
        interest_list.append(EventManager.create(category='Go for a run',duration='40',expiration='180',username='testuser1',building_name='building1',note='test_node'))
        interest_list.append(EventManager.create(category='Go for a run',duration='40',expiration='180',username='testuser2',building_name='building1',note='test_node'))
        interest_list.append(EventManager.create(category='Go for a run',duration='20',expiration='180',username='testuser1',building_name='building1',note='test_node'))

        #Create some activities
        activity_list.append(EventManager.create(category='Go for a run',duration='40',expiration='180',username='testuser',
                                                              building_name ='building1',ip='127.0.0.1',min_number_of_people_to_join='1',max_number_of_people_to_join='1',note='meet me at shadyside'))
        activity_list.append(EventManager.create(category='Play pool',duration='40',expiration='180',username='testuser',
                                                             building_name='building1',ip='127.0.0.1',min_number_of_people_to_join='1',max_number_of_people_to_join='1',note='meet me at shadyside'))

        #Assert if interests and activities are created fine
        self.assertEqual(3,len(Event.get_active_interests_by_category('Go for a run')))
        self.assertEqual(1,len(Event.get_active_activities_by_category('Go for a run')))
        self.assertEqual(1,len(Event.get_active_activities_by_category('Play pool')))


        match_list = MatchMaker.match_all()
        self.assertEqual(2, len(match_list))
        self.assertEqual(2, len(match_list['testuser1']))
        self.assertEqual(1, len(match_list['testuser2']))
        interest = EventManager.create(category='Play pool',duration='40',expiration='180',username='testuser1',building_name='building1',note='test_node')
        interest_list.append(interest)
        match_list = MatchMaker.match_interest_with_activities(interest.key.urlsafe())
        self.assertEqual(1, len(match_list))
        self.assertEqual(1, len(match_list['testuser1']))

        activity = EventManager.create(category='Play pool',duration='40',expiration='180',username='testuser',
                                        building_name ='building1',ip='127.0.0.1',min_number_of_people_to_join='1',max_number_of_people_to_join='1',note='meet me at shadyside')

        match_list = MatchMaker.match_activity_with_interests(activity.key.urlsafe())
        self.assertEqual(1, len(match_list))

        activity = EventManager.create(category='Go for a run',duration='20',expiration='180',username='testuser',
                                                   building_name ='building1',ip='127.0.0.1',min_number_of_people_to_join='1',max_number_of_people_to_join='1',note='meet me at shadyside')

        match_list = MatchMaker.match_activity_with_interests(activity.key.urlsafe())
        self.assertEqual(2, len(match_list))
        self.assertEqual(2, len(match_list['testuser1']))


if __name__ == '__main__':
    unittest.main()


