"""
This file contains stat_routes
"""

from webapp2_extras.routes import RedirectRoute
from web import handlers
from web.joinhour import activity_handler, home_request_handler, join_handler, thank_you_handler, tip_handler
from web.joinhour.post_activity_mgr_handlers import FeedbackEmailHandler


secure_scheme = 'https'

_routes = [
    RedirectRoute('/', home_request_handler.HomeRequestHandler, name='home', strict_slash=True),
    RedirectRoute('/secure/', handlers.SecureRequestHandler, name='secure', strict_slash=True),
    RedirectRoute('/tip/',tip_handler.TipHandler, name='tip', strict_slash=True),
    RedirectRoute('/tip/thankyou/', thank_you_handler.ThankYouHandler, name='thankyou', strict_slash=True),
    RedirectRoute('/activity/', activity_handler.ActivityHandler, name='activity', strict_slash=True),
    RedirectRoute('/join/', join_handler.JoinHandler, name='join', strict_slash=True),
    RedirectRoute('/post_activity_mgr/', FeedbackEmailHandler, name='post_activity_mgr', strict_slash=True)
]

def get_routes():
    return _routes

def add_routes(app):
    if app.debug:
        secure_scheme = 'http'
    for r in _routes:
        app.router.add(r)