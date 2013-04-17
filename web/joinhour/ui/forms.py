__author__ = 'aparbane'

from src.joinhour.modes.feedback.UserFeedback


ACTIVITY_EXPERIENCE = [
    (UserFeedback.NEGATIVE, "Negative"),
    (UserFeedback.NEUTRAL, "Neutral"),
    (UserFeedback.POSITIVE, "Positive"),
    (UserFeedback.VERY_POSITIVE, "Very positive"),
    (UserFeedback.SUPER_POSITIVE, "Super positive")]

class UserFeedbackForm(BaseForm):
    activity_experience = fields.SelectField(_('Activity Experience'),ACTIVITY_EXPERIENCE)

