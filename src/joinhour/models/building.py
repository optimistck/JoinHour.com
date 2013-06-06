__author__ = 'ashahab'
from google.appengine.ext import ndb

class Building(ndb.Model):
    building_name = ndb.StringProperty()
    organization_name = ndb.StringProperty()
    online = ndb.BooleanProperty()
    date_entered = ndb.DateTimeProperty(auto_now_add=True)