from django import template
register = template.Library()

@register.filter
def hr_choices(model, key_name):
    try:
        return getattr(model, 'get_%(key)s_display' % {'key': key_name})()
    except:
        return 'Not Found'
