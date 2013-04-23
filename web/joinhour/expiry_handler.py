__author__ = 'ashahab'
from boilerplate.lib.basehandler import BaseHandler
from src.joinhour.activity_manager import ActivityManager
from src.joinhour.interest_manager import InterestManager
from src.joinhour.models.activity import Activity
from src.joinhour.models.interest import Interest

class ExpiryHandler(BaseHandler):
    """
    Handler for JoinHandler Form
    """

    #TODO: load the categories and sub-categories from the pull-down menu
    def get(self):
        activities =  Activity.query_all_unexpired_activity()

        for activity in activities:
            if activity.status != Activity.COMPLETE and ActivityManager.get(activity.key.urlsafe()).expires_in() == Activity.EXPIRED:
                activity.status = Activity.EXPIRED
                activity.put()

        interests =  Interest.query_all_unexpired_interest()

        for interest in interests:
            if interest.status != Interest.COMPLETE and InterestManager.get(interest.key.urlsafe()).expires_in() == Interest.EXPIRED:
                interest.status = Interest.EXPIRED
                interest.put()