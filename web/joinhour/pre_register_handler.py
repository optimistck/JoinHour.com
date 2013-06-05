import webapp2
from google.appengine.ext import ndb

from boilerplate.lib.basehandler import BaseHandler
from boilerplate import forms
from boilerplate import models
from src.joinhour.models.building import Building
from src.joinhour.models.preregistered_user import Preregistered_User


class PreRegisterHandler(BaseHandler):

    def get(self):
        """ Returns a simple HTML for contact form """

        params = {
            "exception" : self.request.get('exception')
        }
        return self.render_template('preregister.html', **params)
    def post(self):
        """ validate contact form """
        
        building_name = self.form.building_name.data.strip()
        email = self.form.email.data.strip()
        params = {
            "building_name" : building_name,
            "email" : email
        }
        #check whether this building is online
        building_count = Building.query(Building.building_name = building_name, Building.online=True).count()
        if building_count == 0:

        #if online, redirect to full-registration page, with the building and email filled-in

        self.redirect_to('register', **params)
        #if offline, save it, and thank the user


        message = _('Thank you for registering with us We will inform you when the building is ready.')
        self.add_message(message, 'success')
        self.redirect_to('preregister')

    @webapp2.cached_property
    def form(self):
        return forms.LoveForm(self)