from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView


urlpatterns = patterns(
    '',
    url(r'^page1/$', TemplateView.as_view(template_name='demo_app/page1.html'), name='page1'),
    url(r'^page2/$', TemplateView.as_view(template_name='demo_app/page2.html'), name='page2'),
)
