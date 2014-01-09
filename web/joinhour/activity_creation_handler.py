from webapp2_extras.i18n import gettext as _
import webapp2
from boilerplate.external.wtforms.ext import dateutil
from src.joinhour.notification_manager import NotificationManager
from boilerplate.lib.basehandler import BaseHandler, user_required
from boilerplate import forms
from boilerplate import models
import isodate
from src.joinhour.event_manager import EventManager
from datetime import datetime

from boilerplate.external.pytz import timezone
from boilerplate.external.pytz.reference import  Local




class ActivityCreationHandler(BaseHandler):
    """
    Handler for ActivityCreationHandler Form
    """

    @user_required
    def get(self):
        params = {}
        return self.render_template('activity_creation.html', **params)

    @user_required
    def post(self):
        if self.user:
            user_info = models.User.get_by_id(long(self.user_id))
            building_name = user_info.building
            interest_info = dict()
            interest_info['building_name'] = building_name
            interest_info['category'] = self.form.category.data.strip()
            interest_info['username'] = user_info.username
            if hasattr(self.form,'set_time') and self.form.set_time.data != "None" and self.form.set_time.data != "":
                interest_info['start_time'] = isodate.parse_datetime(self.form.set_time.data.strip()).replace(tzinfo=None)
            elif hasattr(self.form,'expiration') and self.form.expiration.data != "" and self.form.expiration.data != "None":
                interest_info['expiration'] = self.form.expiration.data.strip()
            if hasattr(self.form,'min_number_of_people_to_join'):
                interest_info['min_number_of_people_to_join'] = "1" #self.form.min_number_of_people_to_join.data.strip()
            if hasattr(self.form,'max_number_of_people_to_join'):
                interest_info['max_number_of_people_to_join'] = self.form.max_number_of_people_to_join.data.strip()

            ''' Commenting out the logic checking block since the min # to join is always 1 for now'''
            '''
            if hasattr(self.form,'min_number_of_people_to_join') and hasattr(self.form,'max_number_of_people_to_join'):
                min_int = interest_info['min_number_of_people_to_join'].split()[0]
                max_int = interest_info['max_number_of_people_to_join'].split()[0]
                if min_int != 'None' and max_int != 'None':
                    min_count = int(min_int)
                    max_count = int(max_int)
                    if min_count > max_count:
                        message = _("Minimum number of participants cannot be greater than Maximum number of participants.")
                        self.add_message(message, 'error')
                        return self.redirect_to('join')
            '''
            if hasattr(self.form,'meeting_place'):
                interest_info['meeting_place'] = self.form.meeting_place.data.strip()
            if hasattr(self.form,'duration'):
                interest_info['duration'] = self.form.duration.data.strip()
            if hasattr(self.form,'activity_location'):
                interest_info['activity_location'] = self.form.activity_location.data.strip()
            success, message, event = EventManager.create(**interest_info)
            if success:
                message = _("Your post is now live. You can approve join requests and manage it here. Watch your email for notifications.")
                self.add_message(message, 'success')
                email = user_info.email
                self._push_notification(interest_info, email)
            else:
                self.add_message(message, 'error')
            return self.redirect_to('home')

    @webapp2.cached_property
    def form(self):
        return forms.JoinForm(self)

    def _push_notification(self, interest_info, email):

        template_val = {
            "app_name": self.app.config.get('app_name'),
            "activity": interest_info
        }
        notification_manager = NotificationManager.get()
        notification_manager.push_notification(email,
                                               '[ActiMom.com]Activity creation notification',
                                               'emails/activity_created_for_owner.txt',
                                               **template_val)
