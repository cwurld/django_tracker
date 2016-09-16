from django import forms
from django.contrib.auth.models import User

from django.forms.extras.widgets import SelectDateWidget


class StatsSelectorForm(forms.Form):
    start_date = forms.DateField(widget=SelectDateWidget)
    stop_date = forms.DateField(widget=SelectDateWidget)
    user = forms.ChoiceField()
    exclude_anonymous = forms.BooleanField(required=False)
    format = forms.ChoiceField(choices=[['table', 'Table'], ['histogram', 'Histogram']])

    def __init__(self, *args, **kwargs):
        super(StatsSelectorForm, self).__init__(*args, **kwargs)
        users = User.objects.filter(is_superuser=False).order_by('email').values_list('email', flat=True)
        self.fields['user'].choices = [['all', 'All']] + \
            [['anonymous', 'Anonymous']] + \
            [[email, email] for email in users]

    def clean(self):
        cleaned_data = super(StatsSelectorForm, self).clean()
        if cleaned_data['start_date'] > cleaned_data['stop_date']:
            raise forms.ValidationError('Stop date must come after start date.')
        return cleaned_data
