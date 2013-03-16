__author__ = 'aparbane'

import unittest
from google.appengine.ext import testbed
from boilerplate.models import User
from src.joinhour.interest_manager import InterestManager
from src.joinhour.models.interest import Interest

class InterestManagerTest(unittest.TestCase):

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

    def test_create_interest(self):
        InterestManager.create_interest(category='Category1',duration='40',expiration='180',username='testuser1',building_name ='building_1')
        InterestManager.create_interest(category='Category2',duration='40',expiration='180',username='testuser2',building_name ='building_1')
        InterestManager.create_interest(category='Category3',duration='40',expiration='180',username='testuser1',building_name ='building_1')
        InterestManager.create_interest(category='Category4',duration='40',expiration='180',username='testuser3',building_name='building_2')
        InterestManager.create_interest(category='Category5',duration='40',expiration='180',username='testuser4',building_name='building_2')
        self.assertEqual(3,len(Interest.get_interests_by_building('building_1')))
        self.assertEqual(2,len(Interest.get_interests_by_building('building_2')))

    def test_load_interest_mgr(self):
        interest_created = InterestManager.create_interest(category='Category1',duration='40',expiration='180',username='testuser1',building_name ='building_1')
        interest_from_interest_mgr = InterestManager.get(interest_created.key.urlsafe()).get_interest()
        self.assertEqual(interest_created.key.urlsafe(),interest_from_interest_mgr.key.urlsafe())
        self.assertEqual(Interest.INITIATED,interest_from_interest_mgr.status)



