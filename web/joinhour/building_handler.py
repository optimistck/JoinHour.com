import webapp2
from google.appengine.ext import ndb
from webapp2_extras.i18n import gettext as _
from boilerplate.lib.basehandler import BaseHandler, user_required
from boilerplate import forms
from boilerplate import models
from src.joinhour.models.building import Building
from src.joinhour.models.preregistered_user import Preregistered_User
import json

class BuildingHandler(BaseHandler):

    @user_required
    def get(self):
        """ Returns a simple HTML for contact form """
        buildings = Building.query().fetch()
        params = {
            "buildings" : buildings,
            "exception" : self.request.get('exception')
        }

        return self.render_template('buildings.html', **params)

    @user_required
    def post(self):
        """ validate contact form """
        
        building_name = self.form.building_name.data.strip()
        online = self.form.online.data
        building = Building()
        building.building_name = building_name
        building.online = online
        building.put()

        #if offline, save it, and thank the user
        return self.redirect_to("buildings")

    @webapp2.cached_property
    def form(self):
        return forms.BuildingForm(self)
