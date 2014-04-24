__author__ = 'Constantin Kostenko, Aparup'

from urlparse import urlparse

from boilerplate.lib.basehandler import BaseHandler
from src.joinhour.matchmaker import MatchMaker
from src.joinhour.notification_manager import NotificationManager
from google.appengine.ext import ndb
from src.joinhour.models.feedback import UserFeedback, CompanionShipRating
from src.joinhour.models.user_activity import UserActivity
from boilerplate import models
import logging


class ActivityDigestHandler(BaseHandler):
    """
    Handles sending the digest of activities to the group members.
    At the end of activity and interest list composition it pushes the result to notification queue.
    """
    def get(self):
        logging.info("Entered the ActivityDigestHandler")
        #TO DO: for each group determine list of forming interests and activities

        try:
            activity_key = self.request.get('activity_key')
            interest_key = self.request.get('interest')
            activity = ndb.Key(urlsafe=activity_key).get()
            #ID activities which no one have joined yet
            if activity is not None and activity.status == Event.FORMING:
                logging.info("ActivityDigestHandler: this activity is FORMING" + activity)
                #activity.status = Event.COMPLETE_NEEDS_FEEDBACK
                #activity.put()
                #self._handleFeedBack(activity)
                #self._handle_companionship_rating(activity)
                #self._start_activity_closure_process(activity)
            #ID activities with at least one person
            elif activity is not None and activity.status == Event.FORMED_OPEN:
                logging.info("ActivityDigestHandler: this activity is FORMED_OPEN")
                #activity.status = Event.CLOSED
                #activity.put()
        except Exception , e:
            logging.warn(e)

        #KEPT FOR REFERENCE - TEMP
        '''
        try:
            activity_key = self.request.get('activity')
            interest_key = self.request.get('interest')
            match_list = {}
            if activity_key != '':
                match_list = MatchMaker.match_activity_with_interests(activity_key)
            elif interest_key != '':
                match_list = MatchMaker.match_interest_with_activities(interest_key)
            else:
                match_list = MatchMaker.match_all()
            self._process_notification(match_list)
        except Exception , e:
            print e
        '''

    #KEPT FOR REFERENCE - TEMP
    def _process_notification(self,match_list):
        #Fire a notification for each user on their channel
        for user in match_list:
            self._notify_interest_owner(user,match_list[user])

    #KEPT FOR REFERENCE - TEMP
    def _notify_interest_owner(self,username,matches):
        user = models.User.get_by_username(username)

        url_object = urlparse(self.request.url)
        if url_object.port is not None:
            url_str = url_object.scheme + '://' + str(url_object.hostname) + ':' +str(url_object.port)
        else:
            url_str = url_object.scheme + '://' + str(url_object.hostname)
        template_val = {
            "app_name": self.app.config.get('app_name'),
            "interest_creator_name": user.name+' '+user.last_name,
            "matches": matches,
            "url" : url_str
        }
        notification_manager = NotificationManager.get()
        notification_manager.push_notification(user.email,
                                               'ActiMom.com: Digest of forming activities and interests in your group',
                                               'emails/digest_of_activities.txt',
                                               **template_val)




