from src.joinhour.models.event import Event

__author__ = 'ashahab'
from webapp2_extras.i18n import gettext as _
import webapp2
from boilerplate.lib.basehandler import BaseHandler, user_required
from boilerplate import forms
from boilerplate import models
from src.joinhour.event_manager import EventManager
from src.joinhour.notification_manager import NotificationManager

#TODO This needs to be rewritten - Look at EventManager.join_flex_interest()
class ConvertHandler(BaseHandler):
    """
    Handler for JoinHandler Form
    """

    def get(self):
        params = {}
        return self.render_template('activity.html', **params)

    @user_required
    def post(self):
        if self.user:
            interest_id = self.request.get('interest_id')
            event_manager = EventManager.get(interest_id)
            success, message, current_owner, new_owner = event_manager.join_flex_interest(
                user_id=self.user_id,
                min_number_of_people_to_join=self.form.min_number_of_people_to_join.data.strip(),
                max_number_of_people_to_join=self.form.max_number_of_people_to_join.data.strip(),
                meeting_place=self.form.meeting_place.data.strip(),
                activity_location=self.form.activity_location.data.strip())
            if success:
                message = _("Activity details necessary to start are now set. We'll keep you posted on activity status.")
                self._push_notification(new_owner, current_owner, event_manager)
                self.add_message(message, 'success')
                return self.redirect_to('activity')
            else:
                self.add_message(message, 'failure')
                return self.redirect_to('activity')


    @webapp2.cached_property
    def form(self):
        return forms.JoinForm(self)

    def _push_notification(self, activity_owner, interest_owner, event_manager):
        participants_list = event_manager.get_all_companions()
        participants = []
        for participant in participants_list:
            participants.append(str(participant.user.get().name) + ' ' + str(participant.user.get().last_name))

        #To the activity owner
        template_val = {
            "app_name": self.app.config.get('app_name'),
            "owner_name":interest_owner.name+' '+interest_owner.last_name,
            "activity": event_manager.get_event(),
            "activity_owner_name": activity_owner.name+' '+activity_owner.last_name,
            "complete": event_manager.status() == Event.COMPLETE,
            "expires_in": event_manager.expires_in(),
            "participants":''.join(participants)
        }
        notification_manager = NotificationManager.get(self)
        notification_manager.push_notification(interest_owner.email,
                                               '[JoinHour.com]Activity details are now set',
                                               'emails/interest_converted_to_activity.txt',
                                               **template_val)