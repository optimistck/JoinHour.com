__author__ = 'ashahab'
from google.appengine.ext import ndb


class Token(ndb.Model):
    value = ndb.IntegerProperty(default=0)
    date_entered = ndb.DateTimeProperty(auto_now_add=True)
    used = ndb.BooleanProperty(default=False)


    @classmethod
    def match(cls, value):
        return cls.query(cls.value == int(value)).get()

    @classmethod
    def get_next_token(cls):
        return cls.query(cls.used == False).get()
