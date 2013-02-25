"""
This file contains stat_routes
"""

from webapp2_extras.routes import RedirectRoute
from web import handlers
from handlers.ActivityHandler import ActivityHandler 
from handlers.JoinHandler import JoinHandler
from handlers.HomeRequestHandler import HomeRequestHandler



secure_scheme = 'https'

_routes = [
    RedirectRoute('/', HomeRequestHandler, name='home', strict_slash=True),
    RedirectRoute('/secure/', handlers.SecureRequestHandler, name='secure', strict_slash=True),
    RedirectRoute('/tip/', handlers.TipHandler, name='tip', strict_slash=True),
    RedirectRoute('/tip/thankyou/', handlers.ThankYouHandler, name='thankyou', strict_slash=True),
    RedirectRoute('/activity/', ActivityHandler, name='activity', strict_slash=True),
    RedirectRoute('/join/', JoinHandler, name='join', strict_slash=True)
]

def get_routes():
    return _routes

def add_routes(app):
    if app.debug:
        secure_scheme = 'http'
    for r in _routes:
        app.router.add(r)