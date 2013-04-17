__author__ = 'ashahab'

from google.appengine.api import taskqueue
import webapp2
from webapp2_extras import jinja2

class NotificationManager(object):



    @classmethod
    def get(cls):
        return NotificationManager()

    def __init__(self):
        pass

    def push_notification(self, to_email, subject, template, **template_val):
        email_body = jinja2.get_jinja2(factory=jinja2.Jinja2(webapp2.get_app()), app=webapp2.get_app()).render_template(template, **template_val)
        email_url = webapp2.uri_for('taskqueue-send-email')
        taskqueue.add(url=email_url,params={
            'to':to_email,
            'subject' : subject,
            'body' : email_body
        })
