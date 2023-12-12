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


@method_decorator(login_required, name='dispatch')
class TrainingView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        your_scheduled_tranings = ScheduledTraining.objects.filter(
            creator=request.user, ending_time__gte=datetime.now()
        ).order_by('-starting_time')
        ongoing_trainings = ScheduledTraining.objects.filter(
            ending_time__gte=datetime.now(), starting_time__lte=datetime.now()
        ).order_by('-starting_time')
        incoming_training_sessions = ScheduledTraining.objects.filter(starting_time__gte=datetime.now()).order_by('-starting_time')

        return render(
            request, 'training/index.html',
            {
                'your_scheduled_trainings': your_scheduled_tranings,
                'ongoing_trainings': ongoing_trainings,
                'incoming_training_sessions': incoming_training_sessions,
                'time_now': datetime.now()
            }
        )
