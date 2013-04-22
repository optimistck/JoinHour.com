__author__ = 'ashahab'

from google.appengine.api import taskqueue
import webapp2
from webapp2_extras import jinja2

class NotificationManager(object):



    @classmethod
    def get(cls,handler=None):
        if handler is not None:
            return NotificationManager(handler)
        else:
            return NotificationManager()

    def __init__(self,handler=None):
        self._handler = handler

    def push_notification(self, to_email, subject, template, **template_val):
        if self._handler is None:
            email_body = jinja2.get_jinja2(factory=jinja2.Jinja2(webapp2.get_app()), app=webapp2.get_app()).render_template(template, **template_val)
            email_url = webapp2.uri_for('taskqueue-send-email')
        else:
            email_body = self._handler.jinja2.render_template(template, **template_val)
            email_url = self._handler.uri_for('taskqueue-send-email')
        taskqueue.add(url=email_url,params={
            'to':to_email,
            'subject' : subject,
            'body' : email_body
        })
