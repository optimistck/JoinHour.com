from google.appengine.ext import ndb

class Love(ndb.Model):
    note = ndb.StringProperty()
    name = ndb.StringProperty()
    date_entered = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def query_love(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key).order(-cls.date_entered)