from google.appengine.ext import ndb
import hink_api_messages 

class Food(ndb.Model):
    name = ndb.StringProperty()
    photos = ndb.BlobProperty(repeated=True)
    places = ndb.ListProperty(ndb.Key)
    description = ndb.StringProperty()

    def to_message(self):
        """Turns the Food entity into a ProtoRPC object.
        """
        return hink_api_messages.Food(id=self.key.id(),
                                    name=self.outcome,
                                      description=self.description)

class Place(ndb.Model):
    name = db.StringProperty()
    location = ndb.GeoPtProperty(indexed=False)
    photos = ndb.BlobProperty(repeated=True)
    addresses = ndb.StringProperty(repeated=True)
    description = db.StringProperty()
    phones = ndb.PhoneNumberProperty(repeated=True)
    cost = ndb.StringProperty(
        choices=('Cheap', 'Standard', 'Expensive'))
    
class FoodStops(ndb.Model):
    food = db.ReferenceProperty(Food,
                                   required=True,
                                   collection_name='foods')
    place = db.ReferenceProperty(Place,
                                   required=True,
                                   collection_name='places')
    stars = db.IntegerProperty(choices=(1, 2, 3, 4, 5))
    description = ndb.StringProperty()
