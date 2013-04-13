__author__ = 'aparbane'
from boilerplate import models
from boilerplate.lib.basehandler import BaseHandler, user_required




class Avatar(BaseHandler):

    @user_required
    def get(self):
        user_info = models.User.get_by_username(self.request.get('user_name'))
        if user_info is not None:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(user_info.avatar)
            return
        else:
            pass








