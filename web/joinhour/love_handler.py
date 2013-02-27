import models
import webapp2
from boilerplate.lib.basehandler import BaseHandler
from boilerplate import forms
from boilerplate import models
from webapp2_extras.i18n import gettext as _
from src.joinhour.models.activity import Activity
from google.appengine.ext import ndb

class LoveHandler(BaseHandler):


    def get(self):
        """ Returns a simple HTML for contact form """

        if self.user:
            user_info = models.User.get_by_id(long(self.user_id))
            # if user_info.name or user_info.last_name:
            #     self.form.name.data = user_info.name + " " + user_info.last_name
        params = {
            "exception" : self.request.get('exception')
        }

        return self.render_template('love.html', **params)
    def post(self):
        """ validate contact form """

        if not self.form.validate():
            return self.get()
        building_name = "building_name"
        love = models.Love()
        love.parent = ndb.Key("loveKey", building_name)
        love.note = self.form.note.data.strip()
        love.put()

        message = _('Thank you for showing us love.')
        self.add_message(message, 'success')
        return self.redirect_to('contact')

    @webapp2.cached_property
    def form(self):
        return forms.LoveForm(self)