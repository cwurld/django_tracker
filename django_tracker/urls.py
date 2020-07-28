from django.conf.urls import url

import django_tracker.views as views


app_name = 'django_tracker'

urlpatterns = [
    url(r'^stats_selector/$', views.StartStatsSelector.as_view(), name='stats_selector'),
    url(r'^stats_select_user/$', views.StatsSelectUser.as_view(), name='stats_select_user'),
    url(r'^stats_table/$', views.StatsTable.as_view(), name='stats_table'),
    url(r'^stats_histogram/$', views.StatsHistogram.as_view(), name='stats_histogram'),
]
