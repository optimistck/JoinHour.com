from boilerplate import models

__author__ = 'aparbane'

from google.appengine.ext import ndb
import webapp2

from web.joinhour.ui.forms import UserFeedbackForm
from boilerplate.lib.basehandler import BaseHandler, user_required
from src.joinhour.models.feedback import UserFeedback, CompanionShipRating
from wtforms import Form


class UserFeedbackHandler(BaseHandler):

    @user_required
    def get(self):
        params = {}
        user_feedback_key = self.request.get('userfeedback_key')
        if user_feedback_key:
            user_feedback = ndb.Key(urlsafe=user_feedback_key).get()
            self.view.user_feedback = user_feedback
            self.view.companion_ship_ratings = CompanionShipRating.query(CompanionShipRating.activity == user_feedback.activity, CompanionShipRating.rater == models.User.get_by_id(long(self.user_id)).key).fetch()
        return self.render_template('user_feedback.html', **params)

    @user_required
    def post(self):
        user_feedback_key = self.request.get('userfeedback_key')
        if user_feedback_key:
            user_feedback = ndb.Key(urlsafe=user_feedback_key).get()
            activity_exp = self.request.get('activity_exp')
            user_feedback.activity_experience = activity_exp
            user_feedback.status = UserFeedback.CLOSED_WITH_FEEDBACK
            user_feedback.put()
            if activity_exp not in [UserFeedback.NEGATIVE, UserFeedback.NEUTRAL]:
                self.add_message("Your feedback was submitted.", 'success')
                return self.redirect_to('tip')
            else:
                self.add_message("Your feedback was submitted. Please tell us how we can make JoinHour work better for you and hundreds of your neighbors.", 'success')
                return self.redirect_to('contact');


    @webapp2.cached_property
    def form(self):
        return UserFeedbackForm(self)


