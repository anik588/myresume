from django import template

register = template.Library()

@register.filter
def to(value):
    """Return a list from 1 to value (inclusive)."""
    return range(1, value + 1)

@register.filter
def minus(value, arg):
    """Subtract two numbers."""
    return value - arg


from django import template
import re

register = template.Library()

@register.filter(name='split_camel_case')
def split_camel_case(value):
    return re.sub(r'([a-z])([A-Z])', r'\1 \2', value)

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key, '')
