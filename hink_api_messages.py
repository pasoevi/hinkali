from protorpc import messages

class Food(messages.Message):
    id = messages.IntegerField(1)
    name = messages.StringField(2)
    # photos = messages.BlobProperty(repeated=True)
    # places = messages.ListProperty(ndb.Key)
    description = messages.StringField(3)

    
class FoodCollection(messages.Message):
    items = messages.MessageField(Food, 1, repeated=True)


class Place(messages.Message):
    name = messages.StringField(1)
    locationLat = messages.StringField(2)
    locationLon = messages.StringField(3)
    address = messages.StringField(4)
    description = messages.StringField(5)
    phone = messages.StringField(6)
    cost = messages.StringField(7)


class PlaceCollection(messages.Message):
    items = messages.MessageField(Place, 1, repeated=True)
