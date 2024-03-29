__author__ = 'Constantin'
#google imports
import webapp2
from webapp2_extras.i18n import gettext as _

# Boilerplate imports
from boilerplate.lib.basehandler import BaseHandler
from boilerplate import models
import jinja2

class PropManagersHandler(BaseHandler):
    """
    Handler for the terms and conditions
    """
    #orig
    def get(self):
    #        if not self.user:
    #            return self.redirect_to('login')
        params = {}
        return self.render_template('propmanagers.html', **params)

    @webapp2.cached_property
    def form(self):
        return forms.StatForm(self)

