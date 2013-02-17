
#  This file contains the routes for JoinHour.com

from webapp2_extras.routes import RedirectRoute
from web import handlers
from handlers.ActivityHandler import ActivityHandler
from handlers.JoinHandler import JoinHandler



secure_scheme = 'https'

_routes = [
    RedirectRoute('/secure/', handlers.SecureRequestHandler, name='secure', strict_slash=True),
    RedirectRoute('/tip/', handlers.TipHandler, name='tip', strict_slash=True),
    RedirectRoute('/activity/', ActivityHandler, name='stat', strict_slash=True),
    RedirectRoute('/join/', JoinHandler, name='join', strict_slash=True)
]

def get_routes():
    return _routes

def add_routes(app):
    if app.debug:
        secure_scheme = 'http'
    for r in _routes:
        app.router.add(r)