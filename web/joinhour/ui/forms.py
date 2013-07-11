from boilerplate.lib import utils

__author__ = 'aparbane'

from webapp2_extras.i18n import lazy_gettext as _

from src.joinhour.models.feedback import UserFeedback
from boilerplate.forms import BaseForm
from wtforms import fields


ACTIVITY_EXPERIENCE = [
    (UserFeedback.NEGATIVE, "Negative"),
    (UserFeedback.NEUTRAL, "Neutral"),
    (UserFeedback.POSITIVE, "Positive"),
    (UserFeedback.VERY_POSITIVE, "Very positive"),
    (UserFeedback.SUPER_POSITIVE, "Super positive")]

class UserFeedbackForm(BaseForm):
    activity_experience = fields.SelectField(_('Activity Experience'),ACTIVITY_EXPERIENCE)


class CompleteProfileForSocialUserForm(BaseForm):
    building = fields.SelectField(_('Building'), choices=utils.BUILDINGS)
    security_code = fields.TextField(_('Security Code'))

