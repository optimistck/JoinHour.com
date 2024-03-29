"""
This file contains stat_routes
"""

from webapp2_extras.routes import RedirectRoute
from web import handlers
from web.joinhour import get_activity_handler
from web.joinhour import terms_handler
from web.joinhour import activity_handler, home_request_handler, join_handler, thank_you_handler, \
    tip_handler, love_handler, how_request_handler, join_activity_handler, expiry_handler, token_gen_handler, \
    convert_handler, update_activity_handler, leave_activity_handler, propmanagers_handler, pre_register_handler, \
    cancel_activity_handler, next_action_preregistered_handler, building_handler, all_buildings_handler, \
    next_action_thankyou_feedback_handler, activity_creation_handler, interest_creation_handler,\
    about_handler, about_leads_handler
from web.joinhour.complete_profile_social_user_handler import CompleteProfileSocialUserHandler
from web.joinhour.taskqueue_handlers.post_activity_completion_handler import PostActivityCompletionHandler
from web.joinhour.services.user_profile import Avatar
from web.joinhour.taskqueue_handlers import activity_lifecycle_handler, match_making_handler
from web.joinhour.user_profile_handler import UserProfileHandler
from web.joinhour.user_feedback_handler import UserFeedbackHandler
from web.joinhour.join_request_handler import JoinRequestHandler
from web.joinhour.activity_digest_handler import ActivityDigestHandler



secure_scheme = 'https'

_routes = [
    RedirectRoute('/', home_request_handler.HomeRequestHandler, name='home', strict_slash=True),
    RedirectRoute('/terms', terms_handler.TermsHandler, name='terms', strict_slash=True),
    RedirectRoute('/secure/', handlers.SecureRequestHandler, name='secure', strict_slash=True),
    #RedirectRoute('/tip/',tip_handler.TipHandler, name='tip', strict_slash=True),
    #RedirectRoute('/tip/thankyou/', thank_you_handler.ThankYouHandler, name='thankyou', strict_slash=True),
    #RedirectRoute('/activity/', activity_handler.ActivityHandler, name='activity', strict_slash=True),
    RedirectRoute('/pipe/', activity_handler.ActivityHandler, name='pipeline', strict_slash=True),
    RedirectRoute('/join/', join_handler.JoinHandler, name='join', strict_slash=True),
    RedirectRoute('/join_request/', JoinRequestHandler, name='join_request', strict_slash=True),
    RedirectRoute('/act/', activity_creation_handler.ActivityCreationHandler, name='activity', strict_slash=True),
    RedirectRoute('/int/', interest_creation_handler.InterestCreationHandler, name='interest', strict_slash=True),
    RedirectRoute('/about/', about_handler.AboutHandler, name='about', strict_slash=True),
    RedirectRoute('/aboutleads/', about_leads_handler.AboutLeadsHandler, name='aboutleads', strict_slash=True),
    #RedirectRoute('/convert_to_activity/', convert_handler.ConvertHandler, name='convert', strict_slash=True),
    RedirectRoute('/activity_detail/', get_activity_handler.GetActivityHandler, name='activity_detail', strict_slash=True),
    #RedirectRoute('/love/', love_handler.LoveHandler, name='love', strict_slash=True),
    RedirectRoute('/post_activity_completion/', PostActivityCompletionHandler, name='post_activity_completion', strict_slash=True),
    RedirectRoute('/activity_closure/', PostActivityCompletionHandler, name='activity_closure', strict_slash=True),
    RedirectRoute('/how/', how_request_handler.HowRequestHandler, name='how', strict_slash=True),
    RedirectRoute('/join_activity/', join_activity_handler.JoinActivityHandler, name='join_activity', strict_slash=True),
    RedirectRoute('/expire_activities/', expiry_handler.ExpiryHandler, name='expire_activities', strict_slash=True),
    RedirectRoute('/match_maker/', match_making_handler.MatchMakingHandler, name='match_maker', strict_slash=True),
    RedirectRoute('/activity_digest/', ActivityDigestHandler, name='activity_digest', strict_slash=True),
    RedirectRoute('/activity_life_cycle/', activity_lifecycle_handler.ActivityLifeCycleHandler, name='activity_life_cycle', strict_slash=True),
    RedirectRoute('/token_generator/', token_gen_handler.TokenGeneratorHandler, name='token_generator', strict_slash=True),
    RedirectRoute('/user_profile/', UserProfileHandler, name='user_profile', strict_slash=True),
    RedirectRoute('/update_activity_list/', update_activity_handler.UpdateActivityHandler, name='update_activities', strict_slash=True),
    RedirectRoute('/append_event_list/', activity_handler.ActivityHandler, name='update_events', strict_slash=True),
    RedirectRoute('/user/avatar/', Avatar, name='avatar', strict_slash=True),
    RedirectRoute('/leave_activity/', leave_activity_handler.LeaveActivityHandler, name='leave_activity', strict_slash=True),
    RedirectRoute('/cancel_activity/', cancel_activity_handler.CancelActivityHandler, name='cancel_activity', strict_slash=True),
    RedirectRoute('/user_feedback/', UserFeedbackHandler, name='user_feedback', strict_slash=True),
    #RedirectRoute('/propmanagers/', propmanagers_handler.PropManagersHandler, name='propmanagers', strict_slash=True),
    #RedirectRoute('/preregister/', pre_register_handler.PreRegisterHandler, name='preregister', strict_slash=True),
    #RedirectRoute('/buildings/', building_handler.BuildingHandler, name='buildings', strict_slash=True),
    #RedirectRoute('/allbuildings/', all_buildings_handler.AllBuildingHandler, name='allbuildings', strict_slash=True),
    RedirectRoute('/next_action_preregistered/', next_action_preregistered_handler.next_action_PreRegisteredHandler, name='next_action_preregistered', strict_slash=True),
    #RedirectRoute('/next_action_thankyou_feedback/', next_action_thankyou_feedback_handler.next_action_ThankYouFeedbackHandler, name='next_action_thankyou_feedback', strict_slash=True),
    RedirectRoute('/complete_profile_social_user/', CompleteProfileSocialUserHandler, name='complete_profile_social_user', strict_slash=True),


]

def get_routes():
    return _routes

def add_routes(app):
    if app.debug:
        secure_scheme = 'http'
    for r in _routes:
        app.router.add(r)