from django import template

register = template.Library()


# See: http://stackoverflow.com/questions/19998912/django-templatetag-return-true-or-false
@register.filter
def show_django_tracker(request):
    if not request:
        return False

    if hasattr(request, 'user'):
        # Django 1.8 and lower
        user = request.user
    else:
        user = request.request.user
    return user.is_superuser or user.groups.filter(name='django_tracker').exists()
