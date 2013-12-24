__author__ = 'apbanerjee'

import unittest

from google.appengine.ext import testbed
from webapp2_extras.appengine.auth.models import User

from src.joinhour.event_manager import EventManager
from src.joinhour.request_manager import RequestManager

from src.joinhour.models.event import Event
from src.joinhour.models.request import Request

from src.joinhour.utils import *


class RequestManagerTest(unittest.TestCase):

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


    def test_initiate(self):
        #Activity Created by user1
        success, message, activity_created = EventManager.create(category='Category1',duration='40',expiration='180',username=self.user1.username,building_name ='building_1',min_number_of_people_to_join='1',max_number_of_people_to_join='2',note='note1', start_time=datetime.today())
        activity_manager = EventManager.get(activity_created.key.urlsafe())
        self.assertEqual(activity_created.key.urlsafe(),activity_manager.get_event().key.urlsafe())
        request = RequestManager.initiate(activity_key=activity_created.key,interest_owner_key=self.user2.key)
        self.assertIsNotNone(request,"Failed to initiate request")
        request_manager = RequestManager.get(request.key.urlsafe())
        self.assertIsNotNone(request_manager,"Failed to load request manager")
        self.assertEqual(True,request_manager.can_accept(self.user1))

    def test_approve(self):
        #Activity Created by user1
        success, message, activity_created = EventManager.create(category='Category1',duration='40',expiration='180',username=self.user1.username,building_name ='building_1',min_number_of_people_to_join='1',max_number_of_people_to_join='2',note='note1', start_time=datetime.today())
        activity_manager = EventManager.get(activity_created.key.urlsafe())
        self.assertEqual(activity_created.key.urlsafe(),activity_manager.get_event().key.urlsafe())
        request = RequestManager.initiate(activity_key=activity_created.key,interest_owner_key=self.user2.key)
        self.assertIsNotNone(request,"Failed to initiate request")
        request_manager = RequestManager.get(request.key.urlsafe())
        self.assertIsNotNone(request_manager,"Failed to load request manager")
        self.assertEqual(True,request_manager.can_accept(self.user1))
        request_manager.accept(self.user1)
        self.assertEqual(request.ACCEPTED,request.status)



