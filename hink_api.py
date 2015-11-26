"""
Google Cloud Endpoints implementation of the api.

Defined here are the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.
"""

import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote


package = "Hinkali"

class Dish(messages.Message):
    name = messages.StringField(1)

    
class DishCollection(messages.Message):
    items = messages.MessageField(Dish, 1, repeated=True)


STORED_DISHES = DishCollection(items=[
    Dish(name='Khinkali'),
    Dish(name='Khachapuri'),
])

@endpoints.api(name='hinkali', version='v1')
class HinkaliApi(remote.Service):
    """Hinkali API v1."""

    @endpoints.method(message_types.VoidMessage, DishCollection,
                      path='hinkali', http_method='GET',
                      name='dishes.listDish')
    def dishes_list(self, request):
        return STORED_DISHES

    ID_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage,
        id=messages.IntegerField(1, variant=messages.Variant.INT32))

    @endpoints.method(ID_RESOURCE, Dish,
                      path='hinkali/{id}', http_method='GET',
                      name='dishes.getDish')
    def get_greeting(self, request):
        try:
            return STORED_DISHES.items[request.id]
        except(IndexError, TypeError):
            raise endpoints.NotFoundException('Dish {1} not found.'.format(request.id,))
        
                      
    
APPLICATION = endpoints.api_server([HinkaliApi])
