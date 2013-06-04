from webapp2_extras.i18n import gettext as _
import webapp2
from boilerplate.lib.basehandler import BaseHandler, user_required
from boilerplate import forms
from boilerplate import models
from src.joinhour.event_manager import EventManager


class JoinHandler(BaseHandler):
    """
    Handler for JoinHandler Form
    """

    @user_required
    def get(self):
        params = {}
        return self.render_template('join.html', **params)

    @user_required
    def post(self):
        if self.user:
            user_info = models.User.get_by_id(long(self.user_id))
            building_name = user_info.building
            interest_info = dict()
            interest_info['building_name'] = building_name
            interest_info['category'] = self.form.category.data.strip()
            interest_info['username'] = user_info.username
            if hasattr(self.form,'expiration'):
                interest_info['expiration'] = self.form.expiration.data.strip()
            elif hasattr(self.form,'start_time'):
                interest_info['start_time'] = self.form.start_time.data.strip()
            if hasattr(self.form,'min_number_of_people_to_join'):
                interest_info['min_number_of_people_to_join'] = self.form.min_number_of_people_to_join.data.strip()
            if hasattr(self.form,'max_number_of_people_to_join'):
                interest_info['max_number_of_people_to_join'] = self.form.max_number_of_people_to_join.data.strip()
            if hasattr(self.form,'meeting_place'):
                interest_info['meeting_place'] = self.form.meeting_place.data.strip()
            if hasattr(self.form,'duration'):
                interest_info['duration'] = self.form.duration.data.strip()
            if hasattr(self.form,'activity_location'):
                interest_info['activity_location'] = self.form.activity_location.data.strip()
            EventManager.create(**interest_info)
            message = _("Your interest was registered successfully. We are searching for a match ... ")
            self.add_message(message, 'success')
            return self.redirect_to('home')

    @webapp2.cached_property
    def form(self):
        return forms.JoinForm(self)



