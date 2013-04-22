"""
This file contains stat_routes
"""

from webapp2_extras.routes import RedirectRoute
from web import handlers
from web.joinhour import get_activity_handler
from web.joinhour import terms_handler
from web.joinhour import activity_handler, home_request_handler, join_handler, thank_you_handler, \
    tip_handler, love_handler, how_request_handler, join_activity_handler, expiry_handler,match_making_handler, \
    token_gen_handler, convert_handler, update_activity_handler, cancel_activity_handler, activity_lifecycle_handler
from web.joinhour.post_activity_completion_handler import PostActivityCompletionHandler
from web.joinhour.services.user_profile import Avatar
from web.joinhour.user_profile_handler import UserProfileHandler
from web.joinhour.user_feedback_handler import UserFeedbackHandler



secure_scheme = 'https'

_routes = [
    RedirectRoute('/', home_request_handler.HomeRequestHandler, name='home', strict_slash=True),
    RedirectRoute('/terms', terms_handler.TermsHandler, name='terms', strict_slash=True),
    RedirectRoute('/secure/', handlers.SecureRequestHandler, name='secure', strict_slash=True),
    RedirectRoute('/tip/',tip_handler.TipHandler, name='tip', strict_slash=True),
    RedirectRoute('/tip/thankyou/', thank_you_handler.ThankYouHandler, name='thankyou', strict_slash=True),
    RedirectRoute('/activity/', activity_handler.ActivityHandler, name='activity', strict_slash=True),
    RedirectRoute('/join/', join_handler.JoinHandler, name='join', strict_slash=True),
    RedirectRoute('/convert_to_activity/', convert_handler.ConvertHandler, name='convert', strict_slash=True),
    RedirectRoute('/activity_detail/', get_activity_handler.GetActivityHandler, name='activity_detail', strict_slash=True),
    RedirectRoute('/love/', love_handler.LoveHandler, name='love', strict_slash=True),
    RedirectRoute('/post_activity_completion/', PostActivityCompletionHandler, name='post_activity_completion', strict_slash=True),
    RedirectRoute('/how/', how_request_handler.HowRequestHandler, name='how', strict_slash=True),
    RedirectRoute('/join_activity/', join_activity_handler.JoinActivityHandler, name='join_activity', strict_slash=True),
    RedirectRoute('/expire_activities/', expiry_handler.ExpiryHandler, name='expire_activities', strict_slash=True),
    RedirectRoute('/match_maker/', match_making_handler.MatchMakingHandler, name='match_maker', strict_slash=True),
    RedirectRoute('/activity_life_cycle/', activity_lifecycle_handler.ActivityLifeCycleHandler, name='activity_life_cycle', strict_slash=True),
    RedirectRoute('/token_generator/', token_gen_handler.TokenGeneratorHandler, name='token_generator', strict_slash=True),
    RedirectRoute('/user_profile/', UserProfileHandler, name='user_profile', strict_slash=True),
    RedirectRoute('/update_activity_list/', update_activity_handler.UpdateActivityHandler, name='update_activities', strict_slash=True),
    RedirectRoute('/user/avatar/', Avatar, name='avatar', strict_slash=True),
    RedirectRoute('/cancel_activity/', cancel_activity_handler.CancelActivityHandler, name='cancel_activity', strict_slash=True),
    RedirectRoute('/user_feedback/', UserFeedbackHandler, name='user_feedback', strict_slash=True)
]

def get_routes():
    return _routes

def add_routes(app):
    if app.debug:
        secure_scheme = 'http'
    for r in _routes:
        app.router.add(r)