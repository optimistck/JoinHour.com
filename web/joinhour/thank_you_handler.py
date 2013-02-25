__author__ = 'aparbane'

from boilerplate.lib.basehandler import BaseHandler

class ThankYouHandler(BaseHandler):
    """
    Handler for the thank you page(after a user tips)
    """

    def get(self):
        """ Returns a simple HTML (for now) for handling the thank you page """
        params = {}
        return self.render_template('thankyou.html', **params)
