from datetime import datetime, timedelta
from platformaDoKursow.models import ScheduledTraining
from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from platformaDoKursow.forms.course_form import CourseForm
from platformaDoKursow.models import Course, Participant, Chapter, ScheduledTraining
from django.utils.decorators import method_decorator
from platformaDoKursow.forms.chapter_form import ChapterForm


@method_decorator(login_required, name='dispatch')
class RemoveTrainingView(View):
    def post(self, request: HttpRequest, id: int) -> HttpResponse:
        try:
            ScheduledTraining.objects.get(id=id, creator=request.user)
        except ScheduledTraining.DoesNotExist:
            messages.error(request, 'Training not found.')
            return redirect('trainings')

        messages.success(request, 'Successfully unscheduled training.')
        return redirect('trainings')
