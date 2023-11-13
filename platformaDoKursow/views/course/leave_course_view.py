from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from platformaDoKursow.forms.course_form import CourseForm
from platformaDoKursow.models import Course, Participant
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class LeaveCourseView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        try:
            Participant.objects.get(user=request.user, course_id=request.GET.get('course_id')).delete()
        except Participant.DoesNotExist:
            messages.error(request, 'Course not found.')
            return redirect('courses')

        messages.success(request, 'Succesfully left the course.')
        return redirect('courses')
