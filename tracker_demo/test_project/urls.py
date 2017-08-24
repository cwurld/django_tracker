import django

if django.VERSION <= (1, 8):
    from django.conf.urls import patterns, url, include
else:
    from django.conf.urls import url, include

from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

if django.VERSION <= (1, 8):
    urlpatterns = patterns(
        '',
        url(r'^$', TemplateView.as_view(template_name='home.html')),
        url(r'^django_tracker/', include('django_tracker.urls', namespace='django_tracker')),
        url(r'^demo_app/', include('demo_app.urls', namespace='demo_app')),
        url(r'^accounts/', include('allauth.urls')),
        url(r'^admin/', include(admin.site.urls)),
    )
else:
    urlpatterns = [
        url(r'^$', TemplateView.as_view(template_name='home.html')),
        url(r'^django_tracker/', include('django_tracker.urls', namespace='django_tracker')),
        url(r'^demo_app/', include('demo_app.urls', namespace='demo_app')),
        url(r'^accounts/', include('allauth.urls')),
        url(r'^admin/', include(admin.site.urls)),
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
