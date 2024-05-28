# templatetags/form_tags.py
from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})

@register.filter(name='add_conditional_complete_class')
def add_conditional_complete_class(value, condition ):
    print(value, condition )
    if condition:
        return 'text-decoration-line-through text-secondary text-opacity-75'
    else:
        return '' 
