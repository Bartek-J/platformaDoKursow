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
class JoinCourseView(View):
    def post(self, request: HttpRequest) -> HttpResponse:
        try:
            course = Course.objects.get(invitation_token=request.POST.get('invitation_token'))
        except Course.DoesNotExist:
            messages.error(request, 'Course not found.')
            return redirect('courses')

        if course.creator == request.user:
            messages.error(request, 'You cannot join your own course')
            return redirect('courses')

        try:
            Participant(course=course, user=request.user).save()
        except IntegrityError:
            messages.error(request, 'You already joined this course')

        messages.success(request, 'You successfully joined the course.')
        return redirect('course', course.id)
