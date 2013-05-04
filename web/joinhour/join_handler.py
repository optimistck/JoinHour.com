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
            is_create_activity = self.request.get('type_radio') == 'activity'
            user_info = models.User.get_by_id(long(self.user_id))
            building_name = user_info.building
            if is_create_activity:
                EventManager.create_activity(building_name=building_name,category=self.form.category.data.strip(),duration=self.form.duration.data.strip(),expiration = self.form.expiration.data.strip(),
                                                username = user_info.username,note = self.form.note.data.strip(),ip = self.request.remote_addr,
                                                min_number_of_people_to_join = self.form.min_number_of_people_to_join.data.strip(),
                                                max_number_of_people_to_join = self.form.max_number_of_people_to_join.data.strip())
                message = _("Your activity was registered successfully.")
            else:
                EventManager.create_interest(building_name=building_name,category=self.form.category.data.strip(),duration=self.form.duration.data.strip(),expiration = self.form.expiration.data.strip(),
                                                username = user_info.username,note = self.form.note.data.strip())
                message = _("Your interest was registered successfully. We are searching for a match ... ")
            self.add_message(message, 'success')
            return self.redirect_to('home')

    @webapp2.cached_property
    def form(self):
        return forms.JoinForm(self)



