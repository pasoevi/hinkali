import urllib

import jinja2
import webapp2
from google.appengine.ext import ndb

from domain.models.category import Category
from domain.services.category_service import CategoryService
import web.views.helpers.components

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('web/templates'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

DEFAULT_CATALOG_NAME = 'categories'


# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent.  However, the write rate should be limited to
# ~1/second.


def catalog_key(catalog_name=DEFAULT_CATALOG_NAME):
    """Constructs a Datastore key for a Catalog entity.

    We use guestbook_name as the key.
    """
    return ndb.Key('Catalog', catalog_name)


class CategoryList(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        cat = self.request.get('catalog_name', DEFAULT_CATALOG_NAME)
        category_service = CategoryService()
        categories = category_service.get_categories(cat)
        template_values = {
            'categories': categories,
            'catalog_name': urllib.quote_plus(cat)
        }
        template = JINJA_ENVIRONMENT.get_template('categories.html')
        # Write the submission form and the footer of the page
        sign_query_params = urllib.urlencode({'catalog_name':
                                                  cat})
        self.response.write(template.render(template_values))


def get_category_dropdown(categories, selected="", option_attrs="", select_attrs=""):
    return web.views.helpers.components.make_dropdown(categories, selected,
                                                      select_attrs, option_attrs)


class CategoryAdd(webapp2.RequestHandler):
    def post(self):
        catalog_name = self.request.get(
            'catalog_name', DEFAULT_CATALOG_NAME)

        category = Category(parent=catalog_key(catalog_name))
        category.name = self.request.get('name')
        category_service = CategoryService()
        category_service.add_category(category)

        query_params = {'catalog_name': catalog_name}
        self.redirect('/categories?' + urllib.urlencode(query_params))
