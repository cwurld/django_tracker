from django import template

register = template.Library()


# See: http://stackoverflow.com/questions/19998912/django-templatetag-return-true-or-false
@register.filter
def show_django_tracker(view):
    user = view.request.user
    return user.is_superuser or user.groups.filter(name='django_tracker').exists()
