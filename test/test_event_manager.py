__author__ = 'aparbane'

import unittest

from google.appengine.ext import testbed
from webapp2_extras.appengine.auth.models import User

from src.joinhour.event_manager import EventManager
from src.joinhour.models.event import Event


class EventManagerTest(unittest.TestCase):

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

    def test_create_activity(self):
        EventManager.create_activity(category='Category1',duration='40',expiration='180',username='testuser1',building_name ='building_1',min_number_of_people_to_join='1',max_number_of_people_to_join='2',note='note1')
        EventManager.create_activity(category='Category2',duration='40',expiration='180',username='testuser2',building_name ='building_1',min_number_of_people_to_join='1',max_number_of_people_to_join='2',note='note2')
        EventManager.create_activity(category='Category3',duration='40',expiration='180',username='testuser1',building_name ='building_1',min_number_of_people_to_join='1',max_number_of_people_to_join='2',note='note2')
        EventManager.create_activity(category='Category4',duration='40',expiration='180',username='testuser3',building_name='building_2',min_number_of_people_to_join='1',max_number_of_people_to_join='2',note='note3')
        EventManager.create_activity(category='Category5',duration='40',expiration='180',username='testuser4',building_name='building_2',min_number_of_people_to_join='1',max_number_of_people_to_join='2',note='note4')
        self.assertEqual(3,len(Event.get_activities_by_building('building_1')))
        self.assertEqual(2,len(Event.get_activities_by_building('building_2')))

    def test_load_activity_mgr(self):
        activity_created = EventManager.create_activity(category='Category1',duration='40',expiration='180',username='testuser1',building_name ='building_1',min_number_of_people_to_join='1',max_number_of_people_to_join='2',note='note1')
        activity_from_activity_mgr = EventManager.get(activity_created.key.urlsafe()).get_event()
        self.assertEqual(activity_created.key.urlsafe(),activity_from_activity_mgr.key.urlsafe())
        self.assertEqual(Event.INITIATED,activity_from_activity_mgr.status)


    def test_join(self):
        user1 = User(
                    name = "User1_name",
                    last_name = "User1_lastname",
                    email = "user@example.com",
                    password = "foo",
                    username = "user1",
                    building = "building_1"
        )
        user1.put()
        user2 = User(
                    name = "User2_name",
                    last_name = "User2_lastname",
                    email = "user2@example.com",
                    password = "foo",
                    username = "user2",
                    building = "building_1"
        )
        user2.put()
        user3 = User(
            name = "User3_name",
            last_name = "User3_lastname",
            email = "user3@example.com",
            password = "foo",
            username = "user2",
            building = "building_1"
        )
        user3.put()
        user4 = User(
            name = "User4_name",
            last_name = "User4_lastname",
            email = "user4@example.com",
            password = "foo",
            username = "user2",
            building = "building_1"
        )
        user4.put()
        activity_created = EventManager.create_activity(category='Category1',duration='40',expiration='180',username=user1.username,building_name ='building_1',min_number_of_people_to_join='1',max_number_of_people_to_join='2',note='note1')
        activity_manager = EventManager.get(activity_created.key.urlsafe())
        self.assertEqual(activity_created.key.urlsafe(),activity_manager.get_event().key.urlsafe())
        self.assertEqual(True,activity_manager.can_join(user2.key.id())[0])
        activity_manager.connect(user2.key.id())
        self.assertEqual(Event.COMPLETE,activity_created.status)
        self.assertEqual(False,activity_manager.can_join(user2.key.id())[0])
        self.assertEqual(True,activity_manager.can_join(user3.key.id())[0])
        activity_manager.connect(user3.key.id())
        self.assertEqual(False,activity_manager.can_join(user4.key.id())[0])
        self.assertEqual(2,len(activity_manager.get_all_companions()))
        self.assertEqual(3,len(activity_manager.get_all_participants()))

    def test_create_interest(self):
        EventManager.create_interest(category='Category1',duration='40',expiration='180',username='testuser1',building_name ='building_1',note='test_note')
        EventManager.create_interest(category='Category2',duration='40',expiration='180',username='testuser2',building_name ='building_1',note='test_note')
        EventManager.create_interest(category='Category3',duration='40',expiration='180',username='testuser1',building_name ='building_1',note='test_note')
        EventManager.create_interest(category='Category4',duration='40',expiration='180',username='testuser3',building_name='building_2',note='test_note')
        EventManager.create_interest(category='Category5',duration='40',expiration='180',username='testuser4',building_name='building_2',note='test_note')
        self.assertEqual(3,len(Event.get_interests_by_building('building_1')))
        self.assertEqual(2,len(Event.get_interests_by_building('building_2')))

    def test_load_interest_mgr(self):
        interest_created = EventManager.create_interest(category='Category1',duration='40',expiration='180',username='testuser1',building_name ='building_1',note='test_note')
        interest_from_interest_mgr = EventManager.get(interest_created.key.urlsafe()).get_event()
        self.assertEqual(interest_created.key.urlsafe(),interest_from_interest_mgr.key.urlsafe())
        self.assertEqual(Event.INITIATED,interest_from_interest_mgr.status)



