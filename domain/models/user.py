from google.appengine.ext import ndb


class User(ndb.Model):
    name = ndb.StringProperty(indexed=False, required=True)
    photo = ndb.BlobProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)
    password = ndb.StringProperty(indexed=False, required=True)
    register_date = ndb.DateTimeProperty(indexed=False, required=True)
