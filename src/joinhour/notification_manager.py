__author__ = 'ashahab'
from  datetime import datetime
from datetime import timedelta
import os

from google.appengine.ext import ndb
from google.appengine.api.taskqueue import Task

from src.joinhour.models.activity import Activity
from src.joinhour.models.match import Match
from src.joinhour.models.interest import Interest
from src.joinhour.models.user_activity import UserActivity
from src.joinhour.interest_manager import InterestManager
from boilerplate import models
from google.appengine.api import taskqueue
from src.joinhour.utils import *
class NotificationManager(object):

    @classmethod
    def get(email_url):
        return NotificationManager(email_url)

    def __init__(self,app,email_url):
        self.email_url = email_url

    def push_notification(self, to_email, subject, template_name, **template_val):
        body = self.jinja2.render_template(template_name, **template_val)
        taskqueue.add(url = self.email_url,params={
            'to':to_email,
            'subject' : subject,
            'body' : body
        })
