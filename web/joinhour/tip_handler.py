__author__ = 'aparbane'

from boilerplate.lib.basehandler import BaseHandler

class TipHandler(BaseHandler):
    """
    Handler for Tip (rating activity participants)
    """

    def get(self):
        """ Returns a simple HTML (for now) for handling tips form """
        params = {}
        return self.render_template('tip.html', **params)
