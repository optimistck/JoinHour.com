from boilerplate.lib.basehandler import BaseHandler, user_required


class AboutHandler(BaseHandler):
    """
    Handler for AboutHandler Page
    """

    def get(self):
        params = {}
        return self.render_template('about.html', **params)


