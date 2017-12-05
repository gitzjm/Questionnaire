from django import template

register = template.Library()

@register.filter
def count(value):
    l=[]
    for i in value:
        l.append(value.user)
    num=len(set(l))
    return num