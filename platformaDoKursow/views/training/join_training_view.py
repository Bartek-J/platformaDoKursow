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
from platformaDoKursow.forms.chapter_form import ChapterForm
from datetime import datetime


@method_decorator(login_required, name='dispatch')
class JoinTrainingView(View):
    def get(self, request: HttpRequest, id: int) -> HttpResponse:
        try:
            scheduled_traning = ScheduledTraining.objects.get(
                id=id, starting_time__lte=datetime.now(), ending_time__gte=datetime.now()
            )
        except ScheduledTraining.DoesNotExist:
            messages.error(request, 'Training not found')
            return redirect('trainings')

        return render(
            request, 'training/join.html',
            {
                'scheduled_training': scheduled_traning
            }
        )
