__author__ = 'ashahab'
from src.joinhour.models.notification import Notification
from webapp2_extras.i18n import gettext as _
import webapp2
from google.appengine.api import channel

from boilerplate.lib.basehandler import BaseHandler, user_required
from boilerplate import forms
from boilerplate import models
from src.joinhour.event_manager import EventManager
from src.joinhour.request_manager import RequestManager
from src.joinhour.utils import *
from src.joinhour.notification_manager import NotificationManager


class JoinActivityHandler(BaseHandler):
    """
    Handler for JoinHandler Form
    """

    @user_required
    def get(self):
        user_id = self.user_id
        key = self.request.get('key')
        activity_manager = EventManager.get(key)
        activity_user = models.User.get_by_username(activity_manager.get_event().username)
        (success, request) = RequestManager.initiate(activity_key=activity_manager.get_event().key,requester_key=models.User.get_by_username(self.username).key)
        if success:
            message = _("Your request is sent to  " + activity_manager.get_event().username + "for approval")
            self._push_notification(activity_manager,request)
            self.add_message(message, 'success')
            return self.redirect_to('activity')
        else:
            message = _("Failed to send join request")
            self.add_message(message, 'failure')
            return self.redirect_to('activity')

    def post(self):
        return self.redirect_to('activity')

    @webapp2.cached_property
    def form(self):
        return forms.JoinActivityForm(self)

    def _push_notification(self,activity_manager,request):
        #Notification Rule : Notify only the activity owner about the join request
        notification_manager = NotificationManager.get(self)
        activity_user = models.User.get_by_username(activity_manager.get_event().username)
        interest_details = get_interest_details(activity_manager.get_event().key.urlsafe())
        request_details = get_request_details(request.key.urlsafe())
        template_val = notification_manager.get_base_template()
        template_val['interest'] = interest_details
        template_val['request'] = request_details
        notification_manager.push_notification(activity_user.email,'[Actimom.com]Request to join Notification','emails/request_to_join_activity.txt',**template_val)

