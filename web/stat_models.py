from webapp2_extras.appengine.auth.models import User
from google.appengine.ext import ndb

#JH experimental

import cgi
import datetime
import urllib
import webapp2
from google.appengine.ext import db
from google.appengine.api import users


class Greeting(db.Model):
  """Models an individual Guestbook entry with an author, content, and date."""
  author = db.StringProperty()
  content = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)


def guestbook_key(guestbook_name=None):
  """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
  return db.Key.from_path('Guestbook', guestbook_name or 'default_guestbook')

#JH experimental END


# Originally meant to call this ActivityManager, but changed the name to just an Actvity
class Activity(ndb.Model):
    """
    The object that manages the activity from its creation to its completion.
    """

    #: Creation date.
    # created = ndb.DateTimeProperty(auto_now_add=True)
    #created = ndb.IntegerProperty(default=0)
    #: Modification date.
    # updated = ndb.DateTimeProperty(auto_now=True)
    #: User defined unique name, also used as key_name.
    # Not used by OpenID
    # organizer_username = ndb.StringProperty()
    #creator = ndb.StringProperty()
    #: User Name
    # organizer_name = ndb.StringProperty()
    #: User Last Name
    #organizer_last_name = ndb.StringProperty()
    #: User email
    #organizer_email = ndb.StringProperty()
    #: Tells if an activity is active or not
    # active = ndb.BooleanProperty(default=False)
    #: Activity Status field
    activity_status = ndb.StringProperty()
    #(text, user, _created=None)
    def add_activity(text):
      """
      Add a new activity to the datastore.
      
      Parameters
        category:     The category of the activity
        user:     User who is adding the quote
        _created: Allows the caller to override the calculated created 
                    value, used only for testing.
      
      Returns  
        The id of the activity or None if the add failed.
      """
      try:
        now = datetime.datetime.now()
        unique_user = _unique_user(user)
        if _created:
          created = _created
        else:
          created = (now - datetime.datetime(2013, 1, 1)).days
          
        a = Activity(
          activity_status=text
          #created=created, 
          #creator=user, 
         # creation_order = now.isoformat()[:19] + "|" + unique_user,
        )
        a.put()
        return a.key().id()
        #return self.redirect_to('register')
        
      except db.Error:
        return None 
    