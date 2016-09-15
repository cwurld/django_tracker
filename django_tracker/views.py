import datetime

from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from django.utils import timezone

import forms

import dateutil.parser

from utils import read_tracker_file


STATS_SELECTOR_SESSION_KEY = 'STATS_SELECTOR_SESSION_KEY'
ONE_DAY = datetime.timedelta(1)


class StatsSelector(FormView):
    form_class = forms.StatsSelectorForm
    template_name = 'django_tracker/stats_selector.html'

    def get_initial(self):
        now = timezone.now().date()
        return {
            'start_date': timezone.now().date(),
            'stop_date': timezone.now().date()
        }

    def form_valid(self, form):
        params = form.cleaned_data
        params['start_date'] = str(params['start_date'])
        params['stop_date'] = str(params['stop_date'])
        self.request.session[STATS_SELECTOR_SESSION_KEY] = params
        return HttpResponseRedirect(reverse('django_tracker:stats_table'))


class StatsTable(TemplateView):
    template_name = 'django_tracker/stats_table.html'

    def get_context_data(self, **kwargs):
        kwargs = super(StatsTable, self).get_context_data(**kwargs)

        selector = self.request.session[STATS_SELECTOR_SESSION_KEY]
        selector['start_date'] = dateutil.parser.parse(selector['start_date']).date()
        selector['stop_date'] = dateutil.parser.parse(selector['stop_date']).date()
        
        kwargs['data'] = []
        done = False
        the_date = selector['start_date']
        while not done:
            kwargs['data'] += read_tracker_file(the_date)
            the_date += ONE_DAY
            done = (the_date > selector['stop_date'])

        return kwargs
