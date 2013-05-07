from google.appengine.ext import ndb
__author__ = 'ashahab'

class LastPush(ndb.Model):
    last_push = ndb.DateTimeProperty()
    date_entered = ndb.DateTimeProperty(auto_now=True)
