from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='split')
def split_filter(value, delimiter=','):
    if not value:
        return []
    return [item.strip() for item in str(value).split(delimiter)]

@register.filter(name='strip')
def strip_filter(value):
    return str(value).strip() if value else ''

@register.filter(name='fcfa')
def fcfa_filter(value):
    try:
        return f"{int(value):,} FCFA".replace(',', ' ')
    except (ValueError, TypeError):
        return str(value)