from google.appengine.ext import ndb


class Address(ndb.Model):
    street = ndb.StringProperty(indexed=True, required=True)
    number = ndb.IntegerProperty(indexed=False)
    zipcode = ndb.StringProperty(indexed=False)
    # The district and region properties can be separate entities
    district = ndb.StringProperty(indexed=False)
    region = ndb.StringProperty(indexed=False)
    latlng = ndb.GeoPtProperty(indexed=False)
