"""
Google Cloud Endpoints implementation of the api.

Defined here are the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.
"""

import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
from hink_api_messages import Food, FoodCollection


package = "Hinkali"


STORED_FOODS = FoodCollection(items=[
    Food(name='Khinkali'),
    Food(name='Khachapuri'),
])

@endpoints.api(name='hinkali', version='v1')
class HinkaliApi(remote.Service):
    """Hinkali API v1."""

    @endpoints.method(message_types.VoidMessage, FoodCollection,
                      path='hinkali', http_method='GET',
                      name='foods.listFood')
    def foods_list(self, request):
        return STORED_FOODS

    ADD_METHOD_RESOURCE = endpoints.ResourceContainer(
        Food,
        food_name=messages.StringField(1, required=True))

    @endpoints.method(ADD_METHOD_RESOURCE, Food,
                      path='hinkali/{food_name}', http_method='POST',
                      name='foods.addFood')
    def add_food(self, request):
        return Food(name=request.food_name)

    
    ID_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage,
        id=messages.IntegerField(1, variant=messages.Variant.INT32))

    @endpoints.method(ID_RESOURCE, Food,
                      path='hinkali/{id}', http_method='GET',
                      name='foods.getFood')
    def get_food(self, request):
        try:
            return STORED_FOODS.items[request.id]
        except(IndexError, TypeError):
            raise endpoints.NotFoundException('Food {1} not found.'.format(request.id,))
        
                      
    
APPLICATION = endpoints.api_server([HinkaliApi])
