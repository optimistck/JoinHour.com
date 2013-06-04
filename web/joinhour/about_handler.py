__author__ = 'ashahab'
#google imports
import webapp2

# Boilerplate imports
from boilerplate.lib.basehandler import BaseHandler

class AboutHandler(BaseHandler):
    """
    Handler for the terms and conditions
    """
    #orig
    def get(self):
    #        if not self.user:
    #            return self.redirect_to('login')
        params = {}
        return self.render_template('about.html', **params)

    @webapp2.cached_property
    def form(self):
        return forms.StatForm(self)

