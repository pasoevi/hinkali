import urllib

import jinja2
import webapp2
from google.appengine.ext import ndb

import web.views.category
from domain.services.category_service import CategoryService
from domain.services.restaurants import RestaurantService
from domain.models.restaurant import Restaurant
from domain.models.address import Address

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('web/templates'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

DEFAULT_CATALOG_NAME = 'library'


# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent.  However, the write rate should be limited to
# ~1/second.


def catalog_key(catalog_name=DEFAULT_CATALOG_NAME):
    """Constructs a Datastore key for a Catalog entity.

    We use guestbook_name as the key.
    """
    return ndb.Key('Catalog', catalog_name)


class RestaurantList(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        catalog_name = self.request.get(
            'catalog_name', DEFAULT_CATALOG_NAME)
        restaurant_service = RestaurantService()
        restaurants = restaurant_service.get_restaurants(catalog_name)
        category_service = CategoryService()

        categories_html = web.views.category.get_category_dropdown(
            category_service.get_categories('categories'), selected=catalog_name,
            select_attrs='name=catalog_name'
        )
        template_values = {
            'restaurants': restaurants,
            'catalog_name': urllib.quote_plus(catalog_name),
            'categories': categories_html
        }
        template = JINJA_ENVIRONMENT.get_template('browse.html')
        # Write the submission form and the footer of the page
        sign_query_params = urllib.urlencode({'catalog_name':
                                                  catalog_name})
        self.response.write(template.render(template_values))


class RestaurantAdd(webapp2.RequestHandler):
    def post(self):
        catalog_name = self.request.get(
            'catalog_name', DEFAULT_CATALOG_NAME)

        restaurant = Restaurant(parent=catalog_key(catalog_name))
        restaurant.title = self.request.get('name')

        restaurant.put()

        query_params = {'catalog_name': catalog_name}
        self.redirect('/?' + urllib.urlencode(query_params))
