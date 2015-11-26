from google.appengine.ext import ndb


# ai esaa chame komentari
class Category(ndb.Model):
    name = ndb.StringProperty(indexed=False, required=True)
    # Other possible properties: date_added, description
