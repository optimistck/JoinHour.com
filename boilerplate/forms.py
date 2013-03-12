"""
Created on June 10, 2012
@author: peta15
"""

from wtforms import fields
from wtforms import Form
from wtforms import validators
from lib import utils
from webapp2_extras.i18n import lazy_gettext as _
from webapp2_extras.i18n import ngettext, gettext

FIELD_MAXLENGTH = 50 # intended to stop maliciously long input
FIELD_MAXLENGTH_NOTE = 140 # intended to stop maliciously long input


class FormTranslations(object):
    def gettext(self, string):
        return gettext(string)

    def ngettext(self, singular, plural, n):
        return ngettext(singular, plural, n)


class BaseForm(Form):
    
    def __init__(self, request_handler):
        super(BaseForm, self).__init__(request_handler.request.POST)
    def _get_translations(self):
        return FormTranslations()


class CurrentPasswordMixin(BaseForm):
    current_password = fields.TextField(_('Password'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH)])


class PasswordMixin(BaseForm):
    password = fields.TextField(_('Password'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH)])


class ConfirmPasswordMixin(BaseForm):
    c_password = fields.TextField(_('Confirm Password'), [validators.Required(), validators.EqualTo('password', _('Passwords must match.')), validators.Length(max=FIELD_MAXLENGTH)])


class UserMixin(BaseForm):
    username = fields.TextField(_('Username'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH), validators.regexp(utils.ALPHANUMERIC_REGEXP, message=_('Username invalid. Use only letters and numbers.'))])
    name = fields.TextField(_('Name'), [validators.Length(max=FIELD_MAXLENGTH)])
    last_name = fields.TextField(_('Last Name'), [validators.Length(max=FIELD_MAXLENGTH)])
    ##country = fields.SelectField(_('Country'), choices=utils.COUNTRIES)
    ### TODO: make this a building pull down, not a country field
    country = fields.SelectField(_('Country'), choices=utils.COUNTRIES)
    building = fields.SelectField(_('Building'), choices=utils.BUILDINGS)

class UserEdit(BaseForm):
    username = fields.TextField(_('Username'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH), validators.regexp(utils.ALPHANUMERIC_REGEXP, message=_('Username invalid. Use only letters and numbers.'))])
    name = fields.TextField(_('Name'), [validators.Length(max=FIELD_MAXLENGTH)])
    last_name = fields.TextField(_('Last Name'), [validators.Length(max=FIELD_MAXLENGTH)])


class PasswordResetCompleteForm(PasswordMixin, ConfirmPasswordMixin):
    pass


# mobile form does not require c_password as last letter is shown while typing and typing is difficult on mobile
class PasswordResetCompleteMobileForm(PasswordMixin):
    pass


class LoginForm(BaseForm):
    password = fields.TextField(_('Password'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH)], id='l_password')
    username = fields.TextField(_('Username'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH)], id='l_username')


class ContactForm(BaseForm):
    email = fields.TextField(_('Email'), [validators.Required(), validators.Length(min=7, max=FIELD_MAXLENGTH), validators.regexp(utils.EMAIL_REGEXP, message=_('Invalid email address.'))])
    name = fields.TextField(_('Name'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH)])
    message = fields.TextAreaField(_('Message'), [validators.Required(), validators.Length(max=65536)])
    #TO DO: remove. Added to make shit work.
    activity_status = fields.TextAreaField(_('activity_status'), [validators.Required(), validators.Length(max=65536)])

class LoveForm(BaseForm):
    name = fields.TextField(_('Name'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH)])
    message = fields.TextAreaField(_('Message'), [validators.Required(), validators.Length(max=65536)])
    #TO DO: remove. Added to make shit work.
    activity_status = fields.TextAreaField(_('activity_status'), [validators.Required(), validators.Length(max=65536)])

#### JH
class PassiveInterestForm(BaseForm):
    #attribute for the form. added to solve the Error: 'boilerplate.forms.PassiveInterestForm object' has no attribute 'interest' 
    interest = fields.TextField(_('interest'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH)])
    category = fields.SelectField(_('Category'), choices=utils.CATEGORY)
    sub_category = fields.SelectField(_('Sub_Category'), choices=utils.SUBCATEGORY)
    time_chunks = fields.SelectField(_('Time_Chunks'), choices=utils.TIME_CHUNKS)
    time_chunks2 = fields.SelectField(_('Time_Chunks2'), choices=utils.TIME_CHUNKS2)


class FeedbackForm(BaseForm):
    note = fields.TextField(_('note'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH)])

class ActivityDetailForm(BaseForm):
    test_key = fields.TextField(_('test_key'))

class StatForm(BaseForm):
    test_key = fields.TextField(_('test_key'))
### JH

#### JH
class InitiateActvityForm(BaseForm):
    category = fields.SelectField(_('Category'), choices=utils.CATEGORY)
    sub_category = fields.SelectField(_('Sub_Category'), choices=utils.SUBCATEGORY)
    #min_number_of_people_to_join = fields.TextField(_('interest'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH)])
    min_number_of_people_to_join = fields.SelectField(_('min_number_of_people_to_join'), choices=utils.NUMBER_OF_PEOPLE)
    duration = fields.SelectField(_('Time_Chunks'), choices=utils.TIME_CHUNKS)
    expiration = fields.SelectField(_('Time_Chunks2'), choices=utils.TIME_CHUNKS2)
    note = fields.TextField(_('note'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH_NOTE)])


class JoinForm(BaseForm):
    category = fields.SelectField(_('Category'), choices=utils.CATEGORY)
    sub_category = fields.SelectField(_('Sub_Category'), choices=utils.SUBCATEGORY)
    min_number_of_people_to_join = fields.SelectField(_('min_number_of_people_to_join'), choices=utils.NUMBER_OF_PEOPLE_MIN)
    max_number_of_people_to_join = fields.SelectField(_('max_number_of_people_to_join'), choices=utils.NUMBER_OF_PEOPLE_MAX)
    duration = fields.SelectField(_('Time_Chunks'), choices=utils.TIME_CHUNKS)
    expiration = fields.SelectField(_('Time_Chunks2'), choices=utils.TIME_CHUNKS2)
    note = fields.TextField(_('note'), [validators.Required(), validators.Length(max=FIELD_MAXLENGTH_NOTE)])
### JH

class JoinActivityForm(BaseForm):
    activity_id = fields.TextField(_('activity_id'))

class RegisterForm(PasswordMixin, ConfirmPasswordMixin, UserMixin):
    email = fields.TextField(_('Email'), [validators.Required(), validators.Length(min=7, max=FIELD_MAXLENGTH), validators.regexp(utils.EMAIL_REGEXP, message=_('Invalid email address.'))])
    pass


# mobile form does not require c_password as last letter is shown while typing and typing is difficult on mobile
class RegisterMobileForm(PasswordMixin, UserMixin):
    email = fields.TextField(_('Email'), [validators.Required(), validators.Length(min=7, max=FIELD_MAXLENGTH), validators.regexp(utils.EMAIL_REGEXP, message=_('Invalid email address.'))])
    pass


class EditProfileForm(UserMixin):
    pass

class MiniEditProfileForm(UserEdit):
    pass

class EditPasswordForm(PasswordMixin, ConfirmPasswordMixin, CurrentPasswordMixin):
    pass


# mobile form does not require c_password as last letter is shown while typing and typing is difficult on mobile
class EditPasswordMobileForm(PasswordMixin, CurrentPasswordMixin):
    pass


class EditEmailForm(PasswordMixin):
    new_email = fields.TextField(_('Email'), [validators.Required(), validators.Length(min=7, max=FIELD_MAXLENGTH), validators.regexp(utils.EMAIL_REGEXP, message=_('Invalid email address.'))])
    