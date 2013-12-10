from boilerplate.lib.basehandler import BaseHandler, user_required


class PostHandler(BaseHandler):
    """
    Handler for PostHandler Page
    """

    @user_required
    def get(self):
        params = {}
        return self.render_template('post.html', **params)


