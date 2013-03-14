__author__ = 'ashahab'
from webapp2_extras.i18n import gettext as _
from google.appengine.ext import ndb
import webapp2
from boilerplate.lib.basehandler import BaseHandler
from boilerplate import forms
from boilerplate import models
from src.joinhour.activity_manager import ActivityManager
from src.joinhour.models.activity import Activity


class ExpiryHandler(BaseHandler):
    """
    Handler for JoinHandler Form
    """

    #TODO: load the categories and sub-categories from the pull-down menu
    def get(self):
        activities =  Activity.query_all_activity()

        for activity in activities:
            if ActivityManager.get(activity.key.id()).expires_in() == Activity.EXPIRED:
                activity.status = Activity.EXPIRED
                activity.put()