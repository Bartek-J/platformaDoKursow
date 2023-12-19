from datetime import datetime, timedelta
from platformaDoKursow.models import ScheduledTraining
from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from platformaDoKursow.forms.course_form import CourseForm
from platformaDoKursow.models import Course, Participant, Chapter
from django.utils.decorators import method_decorator
from platformaDoKursow.forms.training_form import TrainingForm


@method_decorator(login_required, name='dispatch')
class ScheduleTrainingView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(
            request, 'training/create.html',
            {'form': TrainingForm()}
        )

    def post(self, request: HttpRequest) -> HttpRequest:
        form = TrainingForm(request.POST)

        if form.is_valid():
            form.instance.creator = request.user
            form.instance.time_duration = (form.instance.ending_time - form.instance.starting_time).total_seconds() / 60
            form.save()
            messages.success(request, 'Successfully scheduled training.')
        else:
            messages.error(request, f'Error: {form.errors.as_text()}')

        return redirect('trainings')
