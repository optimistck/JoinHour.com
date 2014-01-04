__author__ = 'apbanerjee'


from boilerplate.lib.basehandler import BaseHandler, user_required
from src.joinhour.request_manager import RequestManager
from boilerplate import models

class InitiateJoinRequestHandler(BaseHandler):

    """
    Initiates JoinRequest Workflow
    """

    @user_required
    def get(self):
        user_id = self.user_id
        key = self.request.get('key')
        user_info = models.User.get_by_id(long(user_id))
        RequestManager.initiate(activity_key=key,interest_owner_key=user_info.key.urlsafe())
        #TODO Initiate Appropriate Notifications

