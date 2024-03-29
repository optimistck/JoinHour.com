config = {

# environment this app is running on: localhost, testing, production
'environment': "production",

# webapp2 sessions
'webapp2_extras.sessions' : {'secret_key': 'klaw98a82aj82hJHDUWEHDjskahuWHJJ482'},

# webapp2 authentication
'webapp2_extras.auth' : {'user_model': 'boilerplate.models.User',
                         'cookie_name': 'session_name'},

# jinja2 templates

# Original, next two lines commented out.
#'webapp2_extras.jinja2' : {'template_path': ['templates','boilerplate/templates', 'admin/templates'],
#                           'environment_args': {'extensions': ['jinja2.ext.i18n']}},

'webapp2_extras.jinja2' : {'template_path': ['templates','templates', 'admin/templates'],
                           'environment_args': {'extensions': ['jinja2.ext.i18n','jinja2.ext.loopcontrols']}},

# application name
'app_name' : "ActiMom",

# the default language code for the application.
# should match whatever language the site uses when i18n is disabled
'app_lang' : 'en',

# Locale code = <language>_<territory> (ie 'en_US')
# to pick locale codes see http://cldr.unicode.org/index/cldr-spec/picking-the-right-language-code
# also see http://www.sil.org/iso639-3/codes.asp
# Language codes defined under iso 639-1 http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
# Territory codes defined under iso 3166-1 alpha-2 http://en.wikipedia.org/wiki/ISO_3166-1
# disable i18n if locales array is empty or None
'locales' : ['en_US', 'es_ES', 'it_IT', 'zh_CN', 'id_ID', 'fr_FR', 'de_DE', 'ru_RU', 'pt_BR', 'cs_CZ'],

# contact page email settings
'contact_sender' : "we@ActiMom.com",
'contact_recipient' : "we@ActiMom.com",

# Password AES Encryption Parameters
'aes_key' : "12_24_32_BYTES_KEY_FOR_PASSWORDS",
'salt' : "_PUT_SALT_HERE_TO_SHA512_PASSWORDS_",

# get your own consumer key and consumer secret by registering at https://dev.twitter.com/apps
# callback url must be: http://[YOUR DOMAIN]/login/twitter/complete
'twitter_consumer_key' : 'PUT_YOUR_TWITTER_CONSUMER_KEY_HERE',
'twitter_consumer_secret' : 'PUT_YOUR_TWITTER_CONSUMER_SECRET_HERE',

#Facebook Login
# get your own consumer key and consumer secret by registering at https://developers.facebook.com/apps
#Very Important: set the site_url= your domain in the application settings in the facebook app settings page
# callback url must be: http://[YOUR DOMAIN]/login/facebook/complete
'fb_api_key' : '464071597013686',
'fb_secret' : '74aaae19be887c436de2b725cc19231a',


#Linkedin Login
#Get you own api key and secret from https://www.linkedin.com/secure/developer
'linkedin_api' : 'PUT_YOUR_LINKEDIN_PUBLIC_KEY_HERE',
'linkedin_secret' : 'PUT_YOUR_LINKEDIN_PUBLIC_KEY_HERE',

# Github login
# Register apps here: https://github.com/settings/applications/new
'github_server' : 'github.com',
'github_redirect_uri' : 'http://www.example.com/social_login/github/complete',
'github_client_id' : 'PUT_YOUR_GITHUB_CLIENT_ID_HERE',
'github_client_secret' : 'PUT_YOUR_GITHUB_CLIENT_SECRET_HERE',

# get your own recaptcha keys by registering at http://www.google.com/recaptcha/
'captcha_public_key' : "6LdFCN4SAAAAANtQRdcob4WF9x69q1Nkf6cBqv7L",
'captcha_private_key' : "6LdFCN4SAAAAAEyZKVBwhQYos2jez4dZWzX4Ma0_",

# Leave blank "google_analytics_domain" if you only want Analytics code
'google_analytics_domain' : "www.JoinHour.com",
'google_analytics_code' : "UA-39128080-1",

# add status codes and templates used to catch and display errors
# if a status code is not listed here it will use the default app engine
# stacktrace error page or browser error page
'error_templates' : {
    403: 'errors/default_error.html',
    404: 'errors/default_error.html',
    500: 'errors/default_error.html',
},

# Enable Federated login (OpenID and OAuth)
# Google App Engine Settings must be set to Authentication Options: Federated Login
'enable_federated_login' : True,

# jinja2 base layout template
'base_layout' : 'base.html',

# send error emails to developers
'send_mail_developer' : False,

# fellas' list
'developers' : (
    ('JoinHour', 'we@joinhour.com'),
),

# ----> ADD MORE CONFIGURATION OPTIONS HERE <----

}
