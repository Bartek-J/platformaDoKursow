from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from platformaDoKursow.forms.course_form import CourseForm
from platformaDoKursow.models import Course, Participant
from django.db import IntegrityError
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class JoinNewCourseView(View):
    def get(self, request: HttpRequest, id: int) -> HttpResponse:
        try:
            course = Course.objects.get(pk=id)
        except Course.DoesNotExist:
            messages.error(request, 'Course not found.')
            return redirect('courses')

        if course.creator == request.user:
            messages.error(request, 'You cannot join your own course')
            return redirect('courses')

        try:
            Participant.objects.get(course=course, user=request.user)
            messages.error(request, 'You already joined this course')
        except Participant.DoesNotExist:
            Participant(course=course, user=request.user).save()
            messages.success(request, 'You successfully joined the course.')
        return redirect('show_course', course.id)
