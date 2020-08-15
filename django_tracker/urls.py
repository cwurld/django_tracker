from django.conf.urls import url
from django.urls import path

import django_tracker.views as views


app_name = 'django_tracker'

urlpatterns = [
    url(r'^stats_selector/$', views.StartStatsSelector.as_view(), name='stats_selector'),
    url(r'^stats_select_user/$', views.StatsSelectUser.as_view(), name='stats_select_user'),
    path('past_2_days/', views.StatsLast2Days.as_view(), name='past_2_days'),
    url(r'^stats_table/$', views.StatsTable.as_view(), name='stats_table'),
    url(r'^stats_histogram/$', views.StatsHistogram.as_view(), name='stats_histogram'),
    url(r'^get_ip_details/$', views.get_ip_details, name='get_ip_details'),
]
