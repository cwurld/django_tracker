from django.urls import path
from django.conf.urls import url, include

from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html')),
    path('django_tracker/', include('django_tracker.urls', namespace='django_tracker')),
    path('another_app/', include('another_app.urls', namespace='demo_app')),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
