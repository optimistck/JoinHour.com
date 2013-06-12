__author__ = 'aparbane'

import unittest

from google.appengine.ext import testbed
from webapp2_extras.appengine.auth.models import User

from src.joinhour.event_manager import EventManager
from src.joinhour.models.event import Event
from src.joinhour.utils import *


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

    def test_create_specific_interest(self):
        EventManager.create(category='Category1',duration='40',expiration='180',username='testuser1',building_name ='building_1',min_number_of_people_to_join='1',max_number_of_people_to_join='2',note='note1')
        EventManager.create(category='Category2',duration='40',expiration='180',username='testuser2',building_name ='building_1',min_number_of_people_to_join='1',max_number_of_people_to_join='2',note='note2')
        EventManager.create(category='Category3',duration='40',expiration='180',username='testuser1',building_name ='building_1',min_number_of_people_to_join='1',max_number_of_people_to_join='2',note='note2')
        EventManager.create(category='Category4',duration='40',expiration='180',username='testuser3',building_name='building_2',min_number_of_people_to_join='1',max_number_of_people_to_join='2',note='note3')
        EventManager.create(category='Category5',duration='40',expiration='180',username='testuser4',building_name='building_2',min_number_of_people_to_join='1',max_number_of_people_to_join='2',note='note4')
        self.assertEqual(3,len(Event.get_activities_by_building('building_1')))
        self.assertEqual(2,len(Event.get_activities_by_building('building_2')))


    def test_load_activity_mgr(self):
        activity_created = EventManager.create(category='Category1',duration='40',expiration='180',username='testuser1',building_name ='building_1',min_number_of_people_to_join='1',max_number_of_people_to_join='2',note='note1')
        activity_from_activity_mgr = EventManager.get(activity_created.key.urlsafe()).get_event()
        self.assertEqual(activity_created.key.urlsafe(),activity_from_activity_mgr.key.urlsafe())
        self.assertEqual(Event.FORMING,activity_from_activity_mgr.status)



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
            username = "user3",
            building = "building_1"
        )
        user3.put()
        user4 = User(
            name = "User4_name",
            last_name = "User4_lastname",
            email = "user4@example.com",
            password = "foo",
            username = "user4",
            building = "building_1"
        )
        user4.put()
        activity_created = EventManager.create(category='Category1',duration='40',expiration='180',username=user1.username,building_name ='building_1',min_number_of_people_to_join='1',max_number_of_people_to_join='2',note='note1')
        activity_manager = EventManager.get(activity_created.key.urlsafe())
        self.assertEqual(activity_created.key.urlsafe(),activity_manager.get_event().key.urlsafe())
        self.assertEqual(True,activity_manager.can_join(user2.key.id())[0])
        activity_manager.connect(user2.key.id())
        self.assertEqual(Event.FORMED_OPEN,activity_created.status)
        self.assertEqual(False,activity_manager.can_join(user2.key.id())[0])
        self.assertEqual(True,activity_manager.can_join(user3.key.id())[0])
        activity_manager.connect(user3.key.id())
        self.assertEqual(Event.FORMED_OPEN,activity_created.status)
        self.assertEqual(False,activity_manager.can_join(user4.key.id())[0])
        self.assertEqual(2,activity_manager.companion_count())
        get_interest_details(activity_created.key.urlsafe())
        #Now have 3 Unjoin activity
        activity_manager.unjoin(user3.key.id())
        self.assertEqual(Event.FORMED_OPEN,activity_created.status)
        self.assertEqual(1,activity_manager.companion_count())
        #Now check if User4 can join
        self.assertEqual(True,activity_manager.can_join(user4.key.id())[0])
        activity_manager.connect(user4.key.id())
        self.assertEqual(2,activity_manager.companion_count())
        self.assertEqual(Event.FORMED_OPEN,activity_created.status)
        activity_manager.unjoin(user4.key.id())
        activity_manager.unjoin(user2.key.id())
        self.assertEqual(Event.FORMING,activity_created.status)
        self.assertEqual(0,activity_manager.companion_count())

    def test_create_flex_interest(self):
        EventManager.create(category='Category1',duration='40',expiration='180',username='testuser1',building_name ='building_1',note='test_note')
        EventManager.create(category='Category2',duration='40',expiration='180',username='testuser2',building_name ='building_1',note='test_note')
        EventManager.create(category='Category3',duration='40',expiration='180',username='testuser1',building_name ='building_1',note='test_note')
        EventManager.create(category='Category4',duration='40',expiration='180',username='testuser3',building_name='building_2',note='test_note')
        EventManager.create(category='Category5',duration='40',expiration='180',username='testuser4',building_name='building_2',note='test_note')
        self.assertEqual(3,len(Event.get_interests_by_building('building_1')))
        self.assertEqual(2,len(Event.get_interests_by_building('building_2')))


    def test_load_interest_mgr(self):
        interest_created = EventManager.create(category='Category1',duration='40',expiration='180',username='testuser1',building_name ='building_1',note='test_note')
        interest_from_interest_mgr = EventManager.get(interest_created.key.urlsafe()).get_event()

        self.assertEqual(interest_created.key.urlsafe(),interest_from_interest_mgr.key.urlsafe())
        self.assertEqual(Event.FORMING,interest_from_interest_mgr.status)

    def test_join_flex_interest(self):
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
            username = "user3",
            building = "building_1"
        )
        user3.put()
        interest_created = EventManager.create(category='Category1',duration='40',expiration='180',username=user1.username,building_name ='building_1',note='test_note')
        interest_manager = EventManager.get(interest_created.key.urlsafe())
        interest_from_interest_mgr = interest_manager.get_event()
        self.assertEqual(interest_created.key.urlsafe(),interest_from_interest_mgr.key.urlsafe())
        self.assertEqual(Event.FORMING,interest_from_interest_mgr.status)
        interest_manager.join_flex_interest(user2.key.id(),min_number_of_people_to_join='2',max_number_of_people_to_join='3')
        self.assertEqual(Event.EVENT_TYPE_SPECIFIC_INTEREST,interest_created.type)
        self.assertEqual(Event.FORMING,interest_created.status)
        self.assertEqual(1,interest_manager.companion_count())
        interest_manager.connect(user3.key.id())
        self.assertEqual(Event.FORMED_OPEN,interest_created.status)
        self.assertEqual(2,interest_manager.companion_count())




