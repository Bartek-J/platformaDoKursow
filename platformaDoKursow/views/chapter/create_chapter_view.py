from platformaDoKursow.forms.chapter_form import ChapterForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from platformaDoKursow.models import Course
from django.contrib import messages
from django.views import View


@method_decorator(login_required, name='dispatch')
class CreateChapterView(View):
    def get(self, request: HttpRequest, course_id: int) -> HttpResponse:
        return render(
            request, 'chapter/create.html',
            {'form': ChapterForm(), 'course_id': course_id}
        )

    def post(self, request: HttpRequest, course_id: int) -> HttpRequest:
        form = ChapterForm(request.POST)
        try:
            course = Course.objects.get(id=course_id, creator=request.user)
        except Course.DoesNotExist:
            messages.error(request, 'Invalid course')
            return self.get(request, course_id)

        if form.is_valid():
            form.instance.course = course
            form.save()
            messages.success(request, 'Successfully added chapter.')
            return redirect('course_details', course.pk)
        else:
            messages.error(request, 'Invalid data.')
            return self.get(request, course_id)
