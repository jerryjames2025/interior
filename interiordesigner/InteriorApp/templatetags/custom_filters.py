from django import template

register = template.Library()

@register.filter(name='has_worker')
def has_worker(user):
    return hasattr(user, 'worker')

@register.filter(name='multiply')
def multiply(value, arg):
    return float(value) * float(arg) 