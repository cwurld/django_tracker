import datetime
import json
import os

from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.utils.http import urlencode

from braces.views import GroupRequiredMixin

import django_tracker.forms as forms

import dateutil.parser

from django_tracker.utils import read_tracker_file, histogram_one_day


ONE_DAY = datetime.timedelta(1)
TRACKER_DIR = os.path.join(settings.MEDIA_ROOT, 'tracker')


class StartStatsSelector(GroupRequiredMixin, FormView):
    form_class = forms.StatsSelectorForm
    template_name = 'django_tracker/stats_selector.html'
    group_required = u'django_tracker'
    raise_exception = True

    def get_initial(self):
        selector = self.request.GET
        if selector:
            initial = selector
            initial['start_date'] = dateutil.parser.parse(selector['start_date']).date()
            initial['stop_date'] = dateutil.parser.parse(selector['stop_date']).date()
        else:
            now = timezone.localtime(timezone.now()).date()
            initial = {
                'start_date': now,
                'stop_date': now
            }
        return initial

    def form_valid(self, form):
        params = form.cleaned_data

        # Need to convert datetimes to string so that params can be serialized.
        params['start_date'] = str(params['start_date'])
        params['stop_date'] = str(params['stop_date'])
        qs = urlencode(params)
        return HttpResponseRedirect(reverse('django_tracker:stats_select_user') + '?' + qs)


class StatsSelectUser(GroupRequiredMixin, FormView):
    form_class = forms.SelectUser
    template_name = 'django_tracker/stats_select_user.html'
    group_required = u'django_tracker'
    raise_exception = True

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['start_date'] = dateutil.parser.parse(self.request.GET['start_date']).date()
        kwargs['stop_date'] = dateutil.parser.parse(self.request.GET['stop_date']).date()
        kwargs['exclude_anonymous'] = self.request.GET['exclude_anonymous'] != 'False'
        return kwargs

    def form_valid(self, form):
        qs = self.request.META['QUERY_STRING'] + '&user={}'.format(form.cleaned_data['user'])
        if form.cleaned_data['format'] == 'table':
            return HttpResponseRedirect(reverse('django_tracker:stats_table') + '?' + qs)
        elif form.cleaned_data['format'] == 'histogram':
            return HttpResponseRedirect(reverse('django_tracker:stats_histogram') + '?' + qs)
        else:
            return HttpResponseRedirect('/')


class StatsDisplayMixin(GroupRequiredMixin):
    group_required = u'django_tracker'
    raise_exception = True

    def get_context_data(self, **kwargs):
        kwargs = super(StatsDisplayMixin, self).get_context_data(**kwargs)
        selector = {}
        selector['start_date'] = dateutil.parser.parse(self.request.GET['start_date']).date()
        selector['stop_date'] = dateutil.parser.parse(self.request.GET['stop_date']).date()
        selector['user'] = self.request.GET['user']
        selector['exclude_anonymous'] = self.request.GET['exclude_anonymous'] == 'True'
        if selector['user'] == 'all':
            kwargs['target_user'] = None
        else:
            kwargs['target_user'] = selector['user']

        kwargs['now'] = timezone.now()
        kwargs['selector'] = selector
        kwargs['geo_locate'] = hasattr(settings, 'GEO_LOCATE_FUNC')
        kwargs['location'] = ''

        qs = self.request.META['QUERY_STRING']
        kwargs['as_table_url'] = reverse('django_tracker:stats_table') + '?' + qs
        kwargs['as_histogram_url'] = reverse('django_tracker:stats_histogram') + '?' + qs
        return kwargs


class StatsTable(StatsDisplayMixin, TemplateView):
    template_name = 'django_tracker/stats_table.html'

    def get_context_data(self, **kwargs):
        kwargs = super(StatsTable, self).get_context_data(**kwargs)

        # Load data files from CSV
        kwargs['data'] = []
        done = False
        the_date = kwargs['selector']['start_date']
        while not done:
            day_data = read_tracker_file(
                TRACKER_DIR, the_date, kwargs['selector']['user'],
                exclude_anonymous=kwargs['selector']['exclude_anonymous']
            )
            kwargs['data'] += day_data
            the_date += ONE_DAY
            done = (the_date > kwargs['selector']['stop_date'])
        return kwargs


class StatsHistogram(StatsDisplayMixin, TemplateView):
    template_name = 'django_tracker/stats_histogram.html'

    def get_context_data(self, **kwargs):
        kwargs = super(StatsHistogram, self).get_context_data(**kwargs)

        histogram_x = []
        histogram_y = []
        done = False
        the_date = kwargs['selector']['start_date']
        while not done:
            histogram_y += histogram_one_day(
                TRACKER_DIR,
                the_date,
                kwargs['selector']['user'],
                exclude_anonymous=kwargs['selector']['exclude_anonymous']
            )
            for hour in range(24):
                dt = datetime.datetime.combine(the_date, datetime.time(hour))
                histogram_x.append(dt.strftime('%Y-%m-%d %H'))

            the_date += ONE_DAY
            done = (the_date > kwargs['selector']['stop_date'])

        kwargs['histogram'] = json.dumps([['Hour', 'Views']] + list(map(list, zip(histogram_x, histogram_y))))
        kwargs['histogram_x'] = json.dumps(histogram_x)

        if kwargs['selector']['user'].startswith('anonymous'):
            ip = kwargs['selector']['user'].split('-')[1]
            if ip != 'all':
                kwargs['location'] = settings.GEO_LOCATE_FUNC(ip)
        return kwargs
