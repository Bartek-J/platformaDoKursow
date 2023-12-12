from django import forms
from platformaDoKursow.models import ScheduledTraining
from django.forms.widgets import DateTimeInput


class TrainingForm(forms.ModelForm):
    class Meta:
        model = ScheduledTraining
        fields = ['title', 'description', 'starting_time', 'ending_time', 'time_duration']
        widgets = {
            'starting_time': DateTimeInput(attrs={'type': 'datetime-local', 'step': 60}),
            'ending_time': DateTimeInput(attrs={'type': 'datetime-local', 'step': 60}),
        }
