from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from platformaDoKursow.forms.course_form import CourseForm
from platformaDoKursow.models import Course, Participant
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class RemoveUserFromCourseView(View):
    def post(self, request: HttpRequest, course_id: int) -> HttpResponse:
        try:
            Participant.objects.get(id=request.POST.get('course_id'), course__creator=request.user).delete()
        except Participant.DoesNotExist:
            messages.error(request, 'User for selected course not found.')
            return redirect('course_details', course_id)

        messages.success(request, 'Succesfully left the course.')
        return redirect('course_details', course_id)
