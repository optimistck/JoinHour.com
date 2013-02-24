__author__ = 'aparbane'

from boilerplate.lib.basehandler import BaseHandler
from google.appengine.api import mail
from google.appengine.api import taskqueue

class FeedbackEmailHandler(BaseHandler):

    FOLLOW_UP_EMAIL_INTERVAL = 172800
    FIRST_FEEDBACK_EMAIL_INTERVAL = 1200

    FEEDBACK_URL = ''

    def post(self,*args):
        email_payload = args[0]
        sender = email_payload['sender']
        subject = email_payload['subject']
        isFollowUp = email_payload['isFollowUp']
        template_val = {
            "app_name": self.app.config.get('app_name'),
            "username": email_payload['username'],
            "feedback_url": self.FEEDBACK_URL,
        }
        if isFollowUp:
            if self._check_if_got_feedback() is not True:
                mail.send_mail(sender=sender,
                               subject=subject,
                               body=self.jinja2.render_template('emails/send_feedback',template_val))
                pass
        else:
            mail.send_mail(sender=sender,
                           subject=subject,
                           body=self.jinja2.render_template('emails/send_feedback',template_val))

            taskqueue.add(url='/post_activity_mgr',queue_name='post_activity_mgr', method='POST',payload=email_payload,eta=self.FOLLOW_UP_EMAIL_INTERVAL)

    def _check_if_got_feedback(self):
        #TODO
        return True











