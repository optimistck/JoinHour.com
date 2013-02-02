"""
This file contains stat_routes
"""

from webapp2_extras.routes import RedirectRoute
from web import handlers



secure_scheme = 'https'

_routes = [
	#BP = BoilerPlate code
    RedirectRoute('/secure/', handlers.SecureRequestHandler, name='secure', strict_slash=True),
    RedirectRoute('/tip/', handlers.TipHandler, name='tip', strict_slash=True)
    #RedirectRoute('/', handlers.HomeRequestHandler, name='home', strict_slash=True)
]

def get_routes():
    return _routes

def add_routes(app):
    if app.debug:
        secure_scheme = 'http'
    for r in _routes:
        app.router.add(r)