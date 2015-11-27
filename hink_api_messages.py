from protorpc import messages

class Food(messages.Message):
    name = messages.StringField(1)
    # photos = messages.BlobProperty(repeated=True)
    # places = messages.ListProperty(ndb.Key)
    description = messages.StringProperty()

    
class FoodCollection(messages.Message):
    items = messages.MessageField(Food, 1, repeated=True)


