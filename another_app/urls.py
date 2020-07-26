from django.conf.urls import url

from django.views.generic.base import TemplateView

app_name = 'another_app'

urlpatterns = [
    url(r'^page1/$', TemplateView.as_view(template_name='another_app/page1.html'), name='page1'),
    url(r'^page2/$', TemplateView.as_view(template_name='another_app/page2.html'), name='page2'),
]
