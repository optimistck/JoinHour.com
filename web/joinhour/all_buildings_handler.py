__author__ = 'ashahab'
import webapp2
from google.appengine.ext import ndb
from webapp2_extras.i18n import gettext as _
from boilerplate.lib.basehandler import BaseHandler, user_required
from boilerplate import forms
from boilerplate import models
from src.joinhour.models.building import Building
from src.joinhour.models.preregistered_user import Preregistered_User
import json

class AllBuildingHandler(BaseHandler):

    def get(self):
        """ Returns a simple HTML for contact form """
        buildings = Building.query().fetch(projection=[Building.building_name])
        building_json = json.dumps([building.to_dict() for building in buildings])
        self.response.headers['Content-Type'] = 'application/json'
        return self.response.out.write(building_json)