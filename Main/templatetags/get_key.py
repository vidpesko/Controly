from django import template

register = template.Library()

@register.filter
def get_key(value: dict, arg: str):
    for key, val in value.items():
        if val == 'Koraki':
            return key
