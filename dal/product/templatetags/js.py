from django.utils.safestring import mark_safe
from django.template import Library

import json


register = Library()


@register.filter(is_safe=True)
def js(obj):
    return mark_safe(json.dumps(obj))

@register.filter(is_safe=True)
def divide(value, arg):
    try:
        return value // arg
    except (ValueError, ZeroDivisionError):
        return None


@register.filter(is_safe=True)
def divide2(value, arg):
    return value * arg