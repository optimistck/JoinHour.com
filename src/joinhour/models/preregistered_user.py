__author__ = 'ashahab'
from google.appengine.ext import ndb

class Preregistered_User(ndb.Model):
    building_name = ndb.StringProperty()
    email = ndb.StringProperty()
    date_entered = ndb.DateTimeProperty(auto_now_add=True)