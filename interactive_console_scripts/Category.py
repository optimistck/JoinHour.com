from google.appengine.ext import ndb

class ActivityName(ndb.Model):
    name = ndb.StringProperty()

    @classmethod
    def query_ActivityName(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key)

#an example of fetching ActivityNames
ActivityNames = ActivityName.query().fetch(5)
for i in ActivityNames:
  print i.name

#an example of adding Activities to the Data Store
a = ActivityName(name="Go for a drink")
a.put()
a = ActivityName(name="Go for a run")
a.put()

