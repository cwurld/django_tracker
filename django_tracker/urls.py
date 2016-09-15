from django.conf.urls import patterns, url

import views


urlpatterns = patterns(
    '',
    url(r'^stats_selector/$', views.StatsSelector.as_view(), name='stats_selector'),
    url(r'^stats_table/$', views.StatsTable.as_view(), name='stats_table'),
    )
