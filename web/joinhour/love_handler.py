import webapp2
from google.appengine.ext import ndb

from boilerplate.lib.basehandler import BaseHandler
from boilerplate import forms
from boilerplate import models
from src.joinhour.models.love import Love


class LoveHandler(BaseHandler):

    def get(self):
        """ Returns a simple HTML for contact form """

        if self.user:
            user_info = models.User.get_by_id(long(self.user_id))
            if user_info.name or user_info.last_name:
                self.form.name.data = user_info.name + " " + user_info.last_name

        params = {
            "exception" : self.request.get('exception')
        }
        building_name = "building_name"
        ancestor_key = ndb.Key("loveKey", building_name)
        self.view.loves = Love.query().fetch(20)
        return self.render_template('love.html', **params)
    def post(self):
        """ validate contact form """
        
        building_name = "building_name"
        love = Love()
        love.parent = ndb.Key("loveKey", building_name)
        love.note = self.form.message.data.strip()
        love.name = self.form.name.data.strip()
        love.put()

        #message = _('Thank you for sending us some love.')
        #self.add_message(message, 'success')
        self.redirect_to('next_action_thankyou_feedback')

    @webapp2.cached_property
    def form(self):
        return forms.LoveForm(self)