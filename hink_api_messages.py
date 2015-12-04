from protorpc import messages


class FoodRequest(messages.Message):
    name = messages.StringField(1)
    description = messages.StringField(2)


class FoodStopRequest(messages.Message):
    place_id = messages.IntegerField(1)
    food_id = messages.IntegerField(2)
    description = messages.StringField(3)
    stars = messages.IntegerField(4)


class Food(messages.Message):
    id = messages.IntegerField(1)
    name = messages.StringField(2)
    # photos = messages.BlobProperty(repeated=True)
    # places = messages.ListProperty(ndb.Key)
    description = messages.StringField(3)

    
class FoodCollection(messages.Message):
    items = messages.MessageField(Food, 1, repeated=True)


class PlaceRequest(messages.Message):
    name = messages.StringField(1)
    locationLat = messages.StringField(2)
    locationLon = messages.StringField(3)
    address = messages.StringField(4)
    description = messages.StringField(5)
    phone = messages.StringField(6)
    cost = messages.StringField(7)


class Place(messages.Message):
    id = messages.IntegerField(1)
    name = messages.StringField(2)
    locationLat = messages.StringField(3)
    locationLon = messages.StringField(4)
    address = messages.StringField(5)
    description = messages.StringField(6)
    phone = messages.StringField(7)
    cost = messages.StringField(8)


class PlaceCollection(messages.Message):
    items = messages.MessageField(Place, 1, repeated=True)


class FoodStop(messages.Message):
    place = messages.MessageField(Place, 1)
    food = messages.MessageField(Food, 2)
    description = messages.StringField(3)
    stars = messages.IntegerField(4)


class FoodStopCollection(messages.Message):
    items = messages.MessageField(FoodStop, 1, repeated=True)
