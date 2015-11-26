from google.appengine.ext import ndb

from address import Address


class Restaurant(ndb.Model):
    name = ndb.TextProperty(indexed=False)
    address = ndb.StructuredProperty(Address)
    added = ndb.DateTimeProperty(indexed=False)
    num_views = ndb.IntegerProperty(indexed=False)
    phone = ndb.StringProperty(indexed=False)
    mobile = ndb.StringProperty(indexed=False)
    
    
