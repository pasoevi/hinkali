from google.appengine.ext import ndb

import hink_api_messages 

class Place(ndb.Model):
    name = ndb.StringProperty()
    location = ndb.GeoPtProperty(indexed=False)
    photos = ndb.BlobProperty(repeated=True)
    addresses = ndb.StringProperty(repeated=True)
    description = ndb.StringProperty()
    phones = ndb.StringProperty(repeated=True)
    cost = ndb.StringProperty(
        choices=('Cheap', 'Standard', 'Expensive'))

    def to_message(self):
        """Turns the Food entity into a ProtoRPC object.
        """
        message = hink_api_messages.Place(name=self.name,
                                          description=self.description)
        message.locationLat = self.location.lat
        message.locationLon = self.location.lon
        for address in self.addresses:
            message.addresses.add(address)
        for phone in self.phones:
            message.phones.add(phone)

        message.cost = self.cost
    
        return message

    @classmethod
    def put_from_message(cls, message):
        """Gets the current user and inserts a score.

        Args:
            message: A ScoreRequestMessage instance to be inserted.

        Returns:
            The Score entity that was inserted.
        """
        entity = Place(name=message.place_name)
        entity.location = ndb.GeoPt(message.locationLat, message.locationLon)
        
        #for address in message.addresses:
         #   entity.addresses.add(address)
        entity.put()
        return entity

class Food(ndb.Model):
    name = ndb.StringProperty()
    photos = ndb.BlobProperty(repeated=True)
    # places = ndb.StructuredProperty(Place, repeated=True) # ndb.Key
    description = ndb.StringProperty()

    def to_message(self):
        """Turns the Food entity into a ProtoRPC object.
        """
        return hink_api_messages.Food(name=self.name,
                                      description=self.description)

    @classmethod
    def put_from_message(cls, message):
        """Gets the current user and inserts a score.

        Args:
            message: A ScoreRequestMessage instance to be inserted.

        Returns:
            The Score entity that was inserted.
        """
        entity = Food(name=message.food_name)
        entity.put()
        return entity
    
class FoodStops(ndb.Model):
    food = ndb.KeyProperty(Food,
                           required=True,
    ) # collection_name='foods'
    place = ndb.KeyProperty(Place,
                            required=True,
    ) # collection_name='places'
    stars = ndb.IntegerProperty(choices=(1, 2, 3, 4, 5))
    description = ndb.StringProperty()
