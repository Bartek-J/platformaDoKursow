from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from platformaDoKursow.forms.course_form import CourseForm
from platformaDoKursow.models import Course
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class CourseEditView(View):
    def get(self, request: HttpRequest, id: int) -> HttpResponse:
        try:
            course = Course.objects.get(id=id)
        except Course.DoesNotExist:
            messages.error(request, 'Course not found.')
            return redirect('courses')

        return render(
            request, 'course/edit.html',
            {'form': CourseForm(instance=course), 'course': course}
        )

    def post(self, request: HttpRequest, id: int) -> HttpResponse:
        try:
            course = Course.objects.get(id=id)
        except Course.DoesNotExist:
            messages.error(request, 'Course not found.')
            return redirect('courses')

        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form = form.save()
            return redirect('course_details', id)
        else:
            messages.error(request, 'Invalid data.')
            return self.get(request, id)
