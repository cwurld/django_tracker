import django

if django.VERSION <= (1, 8):
    from django.conf.urls import patterns, url
else:
    from django.conf.urls import url

from django.views.generic.base import TemplateView


if django.VERSION <= (1, 8):
    urlpatterns = patterns(
        '',
        url(r'^page1/$', TemplateView.as_view(template_name='demo_app/page1.html'), name='page1'),
        url(r'^page2/$', TemplateView.as_view(template_name='demo_app/page2.html'), name='page2'),
    )
else:
    urlpatterns = [
        url(r'^page1/$', TemplateView.as_view(template_name='demo_app/page1.html'), name='page1'),
        url(r'^page2/$', TemplateView.as_view(template_name='demo_app/page2.html'), name='page2'),
    ]
