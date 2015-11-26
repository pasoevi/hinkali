import urllib

import jinja2

SELECT_HTML = "<select %s>%s</select>"
OPTION_HTML = "<option %s>%s</option>"

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('web/templates/helpers'),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


def make_dropdown(items, selected="", select_attrs="", option_attrs=""):
    template_values = {
        'sel_attrs': select_attrs,
        'items': items,
        'selected': selected,
        'catalog_name': urllib.quote_plus('genres')}

    template = JINJA_ENVIRONMENT.get_template('dropdown.html')
    return template.render(template_values)
