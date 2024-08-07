from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

@register.filter
def intdot(value):
    try:
        # Usa intcomma para formatear el valor, luego reemplaza las comas por puntos
        return intcomma(value).replace(',', '.')
    except (ValueError, TypeError):
        return value
