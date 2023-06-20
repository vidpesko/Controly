from django import template

register = template.Library()

@register.filter
def get_value(value: dict, arg: str):
    return value[arg]
