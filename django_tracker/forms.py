import os

from django import forms

from django.forms.widgets import SelectDateWidget
from django.conf import settings

from django_tracker.get_users import get_users
from django_tracker.geo_locate import geo_locate


TRACKER_URL = os.path.join(settings.MEDIA_ROOT, 'tracker')


class StatsSelectorForm(forms.Form):
    start_date = forms.DateField(widget=SelectDateWidget)
    stop_date = forms.DateField(widget=SelectDateWidget)
    exclude_anonymous = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(StatsSelectorForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(StatsSelectorForm, self).clean()
        if cleaned_data['start_date'] > cleaned_data['stop_date']:
            raise forms.ValidationError('Stop date must come after start date.')
        return cleaned_data


class SelectUser(forms.Form):
    user = forms.ChoiceField()
    format = forms.ChoiceField(choices=[['table', 'Table'], ['histogram', 'Histogram']])

    def __init__(self, *args, **kwargs):
        start_date = kwargs.pop('start_date')
        stop_date = kwargs.pop('stop_date')
        exclude_anonymous = kwargs.pop('exclude_anonymous')
        super().__init__(*args, **kwargs)

        user_choices = [('all', 'All')]
        anonymous_users, users = get_users(TRACKER_URL, start_date, stop_date)

        if not exclude_anonymous:
            user_choices += [('anonymous-all', 'All Anonymous')]
            for ip in anonymous_users:
                geo = geo_locate(ip)
                user_choices.append(('anonymous-{}'.format(ip), 'Anonymous: {} {}'.format(ip, geo)))

        for email in users:
            user_choices.append(('user-{}'.format(email), email))

        self.fields['user'].choices = user_choices
