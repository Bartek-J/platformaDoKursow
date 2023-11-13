from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from platformaDoKursow.forms.course_form import CourseForm
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class CreateCourseView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(
            request, 'course/create.html',
            {'form': CourseForm()}
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        form = CourseForm(request.POST)
        if form.is_valid():
            form.instance.creator = request.user
            course = form.save()
            messages.success(request, 'Successfully added course.')
            return redirect('course_details', course.pk)
        else:
            messages.error(request, 'Invalid data.')
            return self.get(request)
