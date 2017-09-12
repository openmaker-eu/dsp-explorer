from django import template
register = template.Library()

@register.filter
def hr_choices(model, key_name):
    return getattr(model, 'get_%s_display' % key_name)()
