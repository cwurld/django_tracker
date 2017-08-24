import django

if django.VERSION <= (1, 8):
    from django.conf.urls import patterns, url
else:
    from django.conf.urls import url

from django.views.generic.base import TemplateView
import views


if django.VERSION <= (1, 8):
    urlpatterns = patterns(
        '',
        url(r'^stats_selector/$', views.StatsSelector.as_view(), name='stats_selector'),
        url(r'^stats_table/$', views.StatsTable.as_view(), name='stats_table'),
        url(r'^stats_histogram/$', views.StatsHistogram.as_view(), name='stats_histogram'),
    )
else:
    urlpatterns = [
        url(r'^stats_selector/$', views.StatsSelector.as_view(), name='stats_selector'),
        url(r'^stats_table/$', views.StatsTable.as_view(), name='stats_table'),
        url(r'^stats_histogram/$', views.StatsHistogram.as_view(), name='stats_histogram'),
        ]
