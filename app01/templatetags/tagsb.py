from django import template

register = template.Library()

@register.filter
def my_count(value):
    l=[]
    for i in value:
        l.append(i.user_id)
    num=len(set(l))
    return num