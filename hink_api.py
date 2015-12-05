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
        return food_entity.to_message()

    @endpoints.method(hink_api_messages.FoodStopRequest, hink_api_messages.FoodStop,
                      path='foodstop', http_method='POST',
                      name='foodstop.addFoodStop')
    def add_food_stop(self, request):
        entity = models.FoodStop.put_from_message(request)
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
            raise endpoints.NotFoundException('Food {0} not found.'.format(request.id,))

    @endpoints.method(ID_RESOURCE, hink_api_messages.FoodStopCollection,
                      path='food/places/{id}', http_method='GET',
                      name='food.getFoodPlaces')
    def get_food_place(self, request):
        try:
            food =  models.Food.get_by_id(request.id)
            entities = models.FoodStop.query(models.FoodStop.food==food.key)
            places = [entity.to_message() for entity in entities]
            return hink_api_messages.FoodStopCollection(items=places)
        except(IndexError, TypeError, AttributeError):
            raise endpoints.NotFoundException('Place {0} not found.'.format(request.id))

    @endpoints.method(ID_RESOURCE, message_types.VoidMessage,
                     path='food/delete/{id}', http_method='POST',
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

    @endpoints.method(ID_RESOURCE, hink_api_messages.FoodStopCollection,
                      path='place/food/{id}', http_method='GET',
                      name='place.getPlaceFood')
    def get_place_food(self, request):
        try:
            place =  models.Place.get_by_id(request.id)
            entities = models.FoodStop.query(models.FoodStop.place==place.key)
            foods = [entity.to_message() for entity in entities]
            return hink_api_messages.FoodStopCollection(items=foods)
        except(IndexError, TypeError, AttributeError):
            raise endpoints.NotFoundException('Place {0} not found.'.format(request.id))

    @endpoints.method(ID_RESOURCE, message_types.VoidMessage,
                     path='place/delete/{id}', http_method='POST',
                     name='place.deletePlace')
    def delete_place(self, request):
        
        try:
            place = models.Place.get_by_id(request.id)
            foods = models.FoodStop.query(models.FoodStop.place==place.key)
            [entity.key.delete() for entity in foods]
            place.key.delete()
            return message_types.VoidMessage()
        except(AttributeError):
            raise endpoints.NotFoundException('Place {0} not found.'.format(request.id))

    @endpoints.method(ID_RESOURCE, message_types.VoidMessage,
                     path='place/food/delete/{id}', http_method='POST',
                     name='food.deleteFoodStop')
    def delete_foodstop(self, request):
        try:
            foodstop = models.FoodStop.get_by_id(request.id)
            foodstop.key.delete()
            return message_types.VoidMessage()
        except(AttributeError):
            raise endpoints.NotFoundException('FoodStop {0} not found.'.format(request.id))
                      
    
APPLICATION = endpoints.api_server([HinkaliApi])
