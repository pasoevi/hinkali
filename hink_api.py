"""
Google Cloud Endpoints implementation of the api.

Defined here are the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.
"""

import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
import hink_api_messages
import models

package = "Hinkali"


@endpoints.api(name='hinkali', version='v1')
class HinkaliApi(remote.Service):
    """Hinkali API v1."""

    @endpoints.method(message_types.VoidMessage,
                      hink_api_messages.FoodCollection,
                      path='food', http_method='GET',
                      name='food.listFood')
    def food_list(self, request):
        items = [entity.to_message() for entity in models.Food.query()]
        return hink_api_messages.FoodCollection(items=items)

    @endpoints.method(hink_api_messages.FoodRequest, hink_api_messages.Food,
                      path='food', http_method='POST',
                      name='food.addFood')
    def add_food(self, request):
        entity = models.Food.put_from_message(request)
        """
        food_stop = models.FoodStop(place=request.place_id, food=entity.key.id())
        food_stop.stars = request.stars
        food_stop.put()
        """
        # food = hink_api_messages.Food(name=request.food_name)
        # food.put()
        return entity.to_message()

    
    ID_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage,
        id=messages.IntegerField(1, variant=messages.Variant.INT32))

    @endpoints.method(ID_RESOURCE, hink_api_messages.Food,
                      path='food/{id}', http_method='GET',
                      name='food.getFood')
    def get_food(self, request):
        try:
            food =  models.Food.get_by_id(request.id)
            return food.to_message()
        except(IndexError, TypeError):
            raise endpoints.NotFoundException('Food {1} not found.'.format(request.id,))
        
                      
    
APPLICATION = endpoints.api_server([HinkaliApi])
