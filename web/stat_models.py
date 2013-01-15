from webapp2_extras.appengine.auth.models import User
from google.appengine.ext import ndb


# Originally meant to call this ActivityManager, but changed the name to just an Actvity
class Activity:
    """
    The object that manages the activity from its creation to its completion.
    """

    #: Creation date.
    created = ndb.DateTimeProperty(auto_now_add=True)
    #: Modification date.
    updated = ndb.DateTimeProperty(auto_now=True)
    #: User defined unique name, also used as key_name.
    # Not used by OpenID
    organizer_username = ndb.StringProperty()
    #: User Name
    organizer_name = ndb.StringProperty()
    #: User Last Name
    organizer_last_name = ndb.StringProperty()
    #: User email
    organizer_email = ndb.StringProperty()
    #: Tells if an activity is active or not
    active = ndb.BooleanProperty(default=False)
    #: Test field
    test_field = ndb.StringProperty()
    
    @classmethod
    def set_test_field(self):
        """ Sets a test field to a string.
        """
        #test_field = "Here is the test field value you asked for"
        return test_field 

    