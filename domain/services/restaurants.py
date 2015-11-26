"""
Hello World API implemented using Google Cloud Endpoints.

Defined here are the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.
"""

from google.appengine.ext import ndb

from domain.models import restaurant

package = 'hinkali'

DEFAULT_CATALOG_NAME = 'restaurants'


def catalog_key(catalog_name=DEFAULT_CATALOG_NAME):
    """Constructs a Datastore key for a Catalog entity.

    We use guestbook_name as the key.
    """
    return ndb.Key('Catalog', catalog_name)


class RestaurantService:
    def __init__(self):
        pass

    def get_restaurants(self, catalog):
        restaurants_query = restaurant.Restaurant.query(
            ancestor=catalog_key(catalog))  
        restaurants = restaurants_query.fetch(10)
        return restaurants



