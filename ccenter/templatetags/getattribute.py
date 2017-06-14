
# For future use...
# in template:
# {% load getattribute %}
# {{ form|getattribute:"char_value" }}
# * It doesn't work as is...
# from: http://stackoverflow.com/questions/844746/performing-a-getattr-style-lookup-in-a-django-template


import re
from django import template
from django.conf import settings

numeric_test = re.compile("^\d+$")
register = template.Library()

def getattribute(value, arg):
    """Gets an attribute of an object dynamically from a string name"""

    return getattr(value, arg)

    if hasattr(value, str(arg)):
        return getattr(value, arg)
    elif hasattr(value, 'has_key') and value.has_key(arg):
        return value[arg]
    elif numeric_test.match(str(arg)) and len(value) > int(arg):
        return value[int(arg)]
    else:
        return settings.TEMPLATE_STRING_IF_INVALID

register.filter('getattribute', getattribute)