from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return None


@register.filter
def startswith(value, prefix):
    return value.startswith(prefix)