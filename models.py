from google.appengine.ext import ndb

import hink_api_messages 

class Place(ndb.Model):
    name = ndb.StringProperty()
    location = ndb.GeoPtProperty(indexed=False)
    photos = ndb.BlobProperty(repeated=True)
    address = ndb.StringProperty()
    description = ndb.StringProperty()
    phone = ndb.StringProperty()
    cost = ndb.StringProperty(
        choices=('Cheap', 'Standard', 'Expensive'))

    def to_message(self):
        """Turns the Food entity into a ProtoRPC object.
        """
        message = hink_api_messages.Place(id=self.key.id())
        message.name=self.name
        message.description=self.description
        message.locationLat = str(self.location.lat)
        message.locationLon = str(self.location.lon)
        
        message.address = self.address
        message.description = self.description
        message.phone = self.phone
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
        entity = Place(name=message.name)
        entity.location = ndb.GeoPt(message.locationLat, message.locationLon)
        entity.address = message.address
        entity.phone = message.phone
        entity.description = message.description
        entity.cost = message.cost
        
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
        message = hink_api_messages.Food(id=self.key.id())
        message.name=self.name
        message.description=self.description
        return message

    @classmethod
    def put_from_message(cls, message):
        """Gets the current user and inserts a score.

        Args:
            message: A ScoreRequestMessage instance to be inserted.

        Returns:
            The Score entity that was inserted.
        """
        entity = Food(name=message.name)
        entity.description = message.description
        entity.put()
        return entity
    
class FoodStop(ndb.Model):
    food = ndb.KeyProperty(Food,
                           required=True,
    ) # collection_name='foods'
    place = ndb.KeyProperty(Place,
                            required=True,
    ) # collection_name='places'
    stars = ndb.IntegerProperty(choices=(1, 2, 3, 4, 5))
    description = ndb.StringProperty()

    def to_message(self):
        """turns the foodstop entity into a protorpc object.
        """
        place_entity = Place.get_by_id(self.place.id())
        food_entity = Food.get_by_id(self.food.id())
        
        message = hink_api_messages.FoodStop()
        message.place = place_entity.to_message()
        message.food = food_entity.to_message()
        message.description = self.description
        message.stars = self.stars
        return message

    @classmethod
    def put_from_message(cls, message):
        """gets the current user and inserts a score.

        args:
            message: a scorerequestmessage instance to be inserted.

        returns:
            the score entity that was inserted.
        """

        food_entity = Food.get_by_id(message.food_id)
        place_entity =  Place.get_by_id(message.place_id)
        food_stop = FoodStop(place=place_entity.key, food=food_entity.key)
        food_stop.stars = message.stars
        food_stop.description = message.description
        food_stop.put()
        return food_stop
