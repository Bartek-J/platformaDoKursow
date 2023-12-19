from django import forms
from platformaDoKursow.models import ScheduledTraining
from django.forms.widgets import DateTimeInput


class TrainingForm(forms.ModelForm):
    class Meta:
        model = ScheduledTraining
        fields = ['title', 'description', 'starting_time', 'ending_time']
        widgets = {
            'starting_time': DateTimeInput(attrs={'type': 'datetime-local', 'step': 60}),
            'ending_time': DateTimeInput(attrs={'type': 'datetime-local', 'step': 60}),
        }

    def clean(self):
        cleaned_data = super().clean()
        starting_time = cleaned_data.get('starting_time')
        ending_time = cleaned_data.get('ending_time')

        if starting_time and ending_time and starting_time >= ending_time:
            self.add_error(None, 'The ending time must be later than the starting time.')

        return cleaned_data
