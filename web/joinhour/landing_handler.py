__author__ = 'Constantin'
#google imports
import webapp2
from webapp2_extras.i18n import gettext as _

# Boilerplate imports
from boilerplate.lib.basehandler import BaseHandler
from boilerplate import models
import jinja2

class LandingHandler(BaseHandler):

    def get(self):
        params = {}
        return self.render_template('landing.html', **params)



