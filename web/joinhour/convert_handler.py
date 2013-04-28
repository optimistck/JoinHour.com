from src.joinhour.models.event import Event

__author__ = 'ashahab'
from webapp2_extras.i18n import gettext as _
import webapp2
from boilerplate.lib.basehandler import BaseHandler, user_required
from boilerplate import forms
from boilerplate import models
from src.joinhour.event_manager import EventManager
from src.joinhour.models.user_activity import UserActivity
from src.joinhour.notification_manager import NotificationManager

class ConvertHandler(BaseHandler):
    """
    Handler for JoinHandler Form
    """

    #TODO: load the categories and sub-categories from the pull-down menu
    def get(self):
        params = {}
        return self.render_template('activity.html', **params)

    @user_required
    def post(self):
        #TODO: the building name needs to come from the user profile


        if self.user:
            user_info = models.User.get_by_id(long(self.user_id))
            building_name = user_info.building
            interest_id = self.request.get('interest_id')

            success, message, interest_owner, activity_key = EventManager.create_activity_from_interest(
                interest_id=interest_id,
                ip=self.request.remote_addr,
                username=user_info.username,
                note=self.form.note.data.strip(),
                min_number_of_people_to_join=self.form.min_number_of_people_to_join.data.strip(),
                max_number_of_people_to_join=self.form.max_number_of_people_to_join.data.strip())
            if success:
                message = _("The interest was converted successfully.")
                self._push_notification(user_info, interest_owner, EventManager.get(activity_key))
                self.add_message(message, 'success')
                return self.redirect_to('activity')
            else:
                self.add_message(message, 'failure')
                return self.redirect_to('activity')


    @webapp2.cached_property
    def form(self):
        return forms.JoinForm(self)

    def _push_notification(self, activity_owner, user_id,activity_manager):
        interest_owner = models.User.get_by_id(long(user_id))
        email_url = self.uri_for('taskqueue-send-email')

        participants_list = UserActivity.query(UserActivity.activity == activity_manager.get_event().key).fetch(projection = [UserActivity.user])
        participants = []
        for participant in participants_list:
            participants.append(str(participant.user.get().name) + ' ' + str(participant.user.get().last_name))

        #To the activity owner
        template_val = {
            "app_name": self.app.config.get('app_name'),
            "owner_name":interest_owner.name+' '+interest_owner.last_name,
            "activity": activity_manager.get_event(),
            "activity_owner_name": activity_owner.name+' '+activity_owner.last_name,
            "complete": activity_manager.status() == Event.COMPLETE,
            "expires_in": activity_manager.expires_in(),
            "participants":''.join(participants)
        }
        notification_manager = NotificationManager.get()
        notification_manager.push_notification(interest_owner.email,
                                               '[JoinHour.com]Your interest is now an Activity',
                                               'emails/interest_converted_to_activity.txt',
                                               **template_val)