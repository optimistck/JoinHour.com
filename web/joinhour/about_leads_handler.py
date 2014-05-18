from boilerplate.lib.basehandler import BaseHandler, user_required


class AboutLeadsHandler(BaseHandler):
    """
    Handler for AboutHandler Page
    """

    def get(self):
        params = {}
        return self.render_template('aboutleads.html', **params)


