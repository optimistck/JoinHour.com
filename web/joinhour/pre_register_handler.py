import webapp2
from google.appengine.ext import ndb

from boilerplate.lib.basehandler import BaseHandler
from boilerplate import forms
from boilerplate import models
from src.joinhour.models.love import Love


class PreRegisterHandler(BaseHandler):

    def get(self):
        """ Returns a simple HTML for contact form """

        params = {
            "exception" : self.request.get('exception')
        }
        return self.render_template('preregister.html', **params)
    def post(self):
        """ validate contact form """
        
        building_name = "building_name"
        love = Love()
        love.parent = ndb.Key("loveKey", building_name)
        love.note = self.form.message.data.strip()
        love.name = self.form.name.data.strip()
        love.put()

#        message = _('Thank you for showing us love.')
#        self.add_message(message, 'success')
        self.redirect_to('love')

    @webapp2.cached_property
    def form(self):
        return forms.LoveForm(self)