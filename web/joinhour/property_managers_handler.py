from webapp2_extras.i18n import gettext as _
from google.appengine.ext import ndb
import webapp2
from boilerplate.lib.basehandler import BaseHandler, user_required

class PropertyManagersHandler(BaseHandler):

    def get(self):
        params = {}
        return self.render_template('property_managers.html', **params)
