import datetime
import json

from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from django.utils import timezone

import forms

import dateutil.parser

from utils import read_tracker_file, histogram_one_day


STATS_SELECTOR_SESSION_KEY = 'STATS_SELECTOR_SESSION_KEY'
ONE_DAY = datetime.timedelta(1)


class StatsSelector(FormView):
    form_class = forms.StatsSelectorForm
    template_name = 'django_tracker/stats_selector.html'

    def get_initial(self):
        now = timezone.localtime(timezone.now()).date()
        return {
            'start_date': now,
            'stop_date': now
        }

    def form_valid(self, form):
        params = form.cleaned_data

        # Need to convert datetimes to string so that params can be serialized.
        params['start_date'] = str(params['start_date'])
        params['stop_date'] = str(params['stop_date'])
        self.request.session[STATS_SELECTOR_SESSION_KEY] = params

        if params['format'] == 'table':
            return HttpResponseRedirect(reverse('django_tracker:stats_table'))
        elif params['format'] == 'histogram':
            return HttpResponseRedirect(reverse('django_tracker:stats_histogram'))
        else:
            return HttpResponseRedirect('/')


class StatsDisplayMixin(object):
    def get_context_data(self, **kwargs):
        kwargs = super(StatsDisplayMixin, self).get_context_data(**kwargs)
        selector = self.request.session[STATS_SELECTOR_SESSION_KEY]
        selector['start_date'] = dateutil.parser.parse(selector['start_date']).date()
        selector['stop_date'] = dateutil.parser.parse(selector['stop_date']).date()
        if selector['user'] == 'all':
            kwargs['target_user'] = None
        else:
            kwargs['target_user'] = selector['user']

        kwargs['now'] = timezone.now()
        kwargs['selector'] = selector
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
            kwargs['data'] += read_tracker_file(
                the_date, exclude_anonymous=kwargs['selector']['exclude_anonymous'], target_user=kwargs['target_user'])
            the_date += ONE_DAY
            done = (the_date > kwargs['selector']['stop_date'])
        return kwargs


class StatsHistogram(StatsDisplayMixin, TemplateView):
    template_name = 'django_tracker/stats_histogram.html'

    def get_context_data(self, **kwargs):
        kwargs = super(StatsHistogram, self).get_context_data(**kwargs)

        histogram_y = []
        histogram_x = []
        one_day = map(str, range(0, 24))
        done = False
        the_date = kwargs['selector']['start_date']
        while not done:
            histogram_y += histogram_one_day(
                the_date,
                exclude_anonymous=kwargs['selector']['exclude_anonymous'],
                target_user=kwargs['target_user']
            )
            histogram_x += one_day
            the_date += ONE_DAY
            done = (the_date > kwargs['selector']['stop_date'])

        kwargs['histogram'] = json.dumps([['Hour', 'Views']] + map(list, zip(histogram_x, histogram_y)))
        kwargs['histogram_x'] = json.dumps(histogram_x)
        return kwargs
