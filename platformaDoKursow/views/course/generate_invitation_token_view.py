from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from platformaDoKursow.forms.course_form import CourseForm
from platformaDoKursow.models import Course
from uuid import uuid4
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class GenerateInvitationTokenView(View):
    def post(self, request: HttpRequest, id: int) -> HttpResponse:
        try:
            course = Course.objects.get(id=id)

        except Course.DoesNotExist:
            messages.error(request, 'Course not found.')
            return redirect('courses')

        course.invitation_token = str(uuid4())
        course.save()

        return redirect('course_details', id)
