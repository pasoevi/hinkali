"""
Google Cloud Endpoints implementation of the api.

Defined here are the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.
"""

import endpoints
import pprint
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
        food_entity = models.Food.put_from_message(request)
        
        place_entity =  models.Place.get_by_id(int(request.place_id))
        pprint.pprint(place_entity)
        food_stop = models.FoodStop(place=place_entity.key, food=food_entity.key)
        food_stop.stars = request.stars
        food_stop.put()

        
        return food_entity.to_message()

    
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
            raise endpoints.NotFoundException('Food {0} not found.'.format(request.id,))

    @endpoints.method(ID_RESOURCE, message_types.VoidMessage,
                     path='food/{id}', http_method='POST',
                     name='food.deleteFood')
    def delete_food(self, request):
        try:
            food = models.Food.get_by_id(request.id)
            food.key.delete()
            return message_types.VoidMessage()
        except(AttributeError):
            raise endpoints.NotFoundException('Food {0} not found.'.format(request.id))
    
    @endpoints.method(message_types.VoidMessage,
                      hink_api_messages.PlaceCollection,
                      path='place', http_method='GET',
                      name='place.listPlaces')
    def places_list(self, request):
        items = [entity.to_message() for entity in models.Place.query()]
        return hink_api_messages.PlaceCollection(items=items)

    @endpoints.method(hink_api_messages.PlaceRequest, hink_api_messages.Place,
                      path='place', http_method='POST',
                      name='place.addPlace')
    def add_place(self, request):
        entity = models.Place.put_from_message(request)
        return entity.to_message()

    @endpoints.method(ID_RESOURCE, hink_api_messages.Place,
                      path='place/{id}', http_method='GET',
                      name='place.getPlace')
    def get_place(self, request):
        try:
            place =  models.Place.get_by_id(request.id)
            return place.to_message()
        except(IndexError, TypeError, AttributeError):
            raise endpoints.NotFoundException('Place {0} not found.'.format(request.id))

    @endpoints.method(ID_RESOURCE, message_types.VoidMessage,
                     path='place/{id}', http_method='POST',
                     name='place.deletePlace')
    def delete_place(self, request):
        try:
            place = models.Place.get_by_id(request.id)
            place.key.delete()
            return message_types.VoidMessage()
        except(AttributeError):
            raise endpoints.NotFoundException('Place {0} not found.'.format(request.id))
                      
    
APPLICATION = endpoints.api_server([HinkaliApi])
