from django import template
from django.conf import settings


register = template.Library()


# See: http://stackoverflow.com/questions/19998912/django-templatetag-return-true-or-false
@register.filter
def show_django_tracker(request):
    if not request:
        return False
    user = request.request.user
    return user.is_superuser or user.groups.filter(name='django_tracker').exists()


@register.simple_tag()
def geo_locate(ip):
    geo = settings.GEO_LOCATE_FUNC(ip)
    return geo
