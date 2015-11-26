from google.appengine.ext import ndb

from domain.models import category

DEFAULT_CATALOG_NAME = 'genres'


def catalog_key(catalog_name=DEFAULT_CATALOG_NAME):
    """Constructs a Datastore key for a Catalog entity.

    We use guestbook_name as the key.
    """
    return ndb.Key('Catalog', catalog_name)


class CategoryService:
    def __init__(self):
        pass

    def get_categories(self, catalog):
        categories_query = category.Category.query(
            ancestor=catalog_key(catalog))  # .order(-Organisation.release_date)
        categories = categories_query.fetch(10)
        return categories

    def add_category(self, category):
        """
        :param category:
        :return: nothing
        """
        category.put()
