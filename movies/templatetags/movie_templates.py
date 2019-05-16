from django import template

register = template.Library()

@register.filter(name='get_backdrop')
def get_backdrop(value):
    return value.backdrop_url
    
@register.filter(name='get_title')
def get_title(value):
    return value.title
    
@register.filter(name='runtime')
def get_time(value):
    h = value // 60
    m = value % 60
    return str(h) + '시간' + str(m) + '분'