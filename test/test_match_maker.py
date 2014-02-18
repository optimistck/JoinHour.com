

__author__ = 'aparbane'

import unittest
from google.appengine.ext import testbed
from src.joinhour.matchmaker import MatchMaker
from src.joinhour.event_manager import EventManager
from src.joinhour.models.event import Event
from webapp2_extras.appengine.auth.models import User

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
        self.user1 = User(
                    name = "User1_name",
                    last_name = "User1_lastname",
                    email = "user@example.com",
                    password = "foo",
                    username = "user1",
                    building = "building_1"
        )
        self.user1.put()
        self.user2 = User(
                    name = "User2_name",
                    last_name = "User2_lastname",
                    email = "user2@example.com",
                    password = "foo",
                    username = "user2",
                    building = "building_1"
        )
        self.user2.put()
        self.user3 = User(
            name = "User3_name",
            last_name = "User3_lastname",
            email = "user3@example.com",
            password = "foo",
            username = "user3",
            building = "building_1"
        )
        self.user3.put()
        self.user4 = User(
            name = "User4_name",
            last_name = "User4_lastname",
            email = "user4@example.com",
            password = "foo",
            username = "user4",
            building = "building_1"
        )
        self.user4.put()


    def tearDown(self):
        self.testbed.deactivate()

    def test_match_making(self):
        interest_list = []
        activity_list = []
        #Create some interests
        interest_list.append(EventManager.create(category='Play date',duration='40',expiration='180',username='user1',building_name='building1',note='test_node')[2])
        interest_list.append(EventManager.create(category='Play date',duration='40',expiration='180',username='user2',building_name='building1',note='test_node')[2])
        interest_list.append(EventManager.create(category='Play date',duration='20',expiration='180',username='user1',building_name='building1',note='test_node')[2])

        #Create some activities
        activity_list.append(EventManager.create(category='Play date',duration='40',expiration='180',username='user4',
                                                              building_name ='building1',ip='127.0.0.1',min_number_of_people_to_join='1',max_number_of_people_to_join='1',note='meet me at shadyside')[2])
        activity_list.append(EventManager.create(category='Stroller walk',duration='40',expiration='180',username='user4',
                                                             building_name='building1',ip='127.0.0.1',min_number_of_people_to_join='1',max_number_of_people_to_join='1',note='meet me at shadyside')[2])

        #Assert if interests and activities are created fine
        self.assertEqual(3,len(Event.get_active_interests_by_category('Play date')))
        self.assertEqual(1,len(Event.get_active_activities_by_category('Stroller walk')))
        self.assertEqual(1,len(Event.get_active_activities_by_category('Stroller walk')))


        match_list = MatchMaker.match_all()
        self.assertEqual(2, len(match_list))
        self.assertEqual(2, len(match_list['user1']))
        self.assertEqual(1, len(match_list['user2']))
        interest = EventManager.create(category='Stroller walk',duration='40',expiration='180',username='user1',building_name='building1',note='test_node')[2]
        interest_list.append(interest)
        match_list = MatchMaker.match_interest_with_activities(interest.key.urlsafe())
        self.assertEqual(1, len(match_list))
        self.assertEqual(1, len(match_list['user1']))

        activity = EventManager.create(category='Stroller walk',duration='40',expiration='180',username='user4',
                                        building_name ='building1',ip='127.0.0.1',min_number_of_people_to_join='1',max_number_of_people_to_join='1',note='meet me at shadyside')[2]

        match_list = MatchMaker.match_activity_with_interests(activity.key.urlsafe())
        self.assertEqual(1, len(match_list))

        activity = EventManager.create(category='Play date',duration='20',expiration='180',username='user4',
                                                   building_name ='building1',ip='127.0.0.1',min_number_of_people_to_join='1',max_number_of_people_to_join='1',note='meet me at shadyside')[2]

        match_list = MatchMaker.match_activity_with_interests(activity.key.urlsafe())
        self.assertEqual(2, len(match_list))
        self.assertEqual(2, len(match_list['user1']))


if __name__ == '__main__':
    unittest.main()


