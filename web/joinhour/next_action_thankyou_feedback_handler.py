import webapp2
from google.appengine.ext import ndb
from webapp2_extras.i18n import gettext as _
from boilerplate.lib.basehandler import BaseHandler
from boilerplate import models



class next_action_ThankYouFeedbackHandler(BaseHandler):

    def get(self):
        params = {
            "exception" : self.request.get('exception')
        }
        return self.render_template('next_action_thankyou_feedback.html', **params)



