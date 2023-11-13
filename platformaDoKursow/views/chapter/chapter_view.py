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
class ChapterView(View):
    def get(self, request: HttpRequest, course_id: int, id: int) -> HttpResponse:
        try:
            chapter = Chapter.objects.get(course_id=course_id, id=id)
        except Chapter.DoesNotExist:
            messages.error(request, 'Chapter not found')
            return redirect('course_details', course_id)
        return render(
            request, 'chapter/index.html',
            {'form': ChapterForm(instance=chapter), 'course_id': course_id, 'chapter_id': chapter.pk}
        )

    def post(self, request: HttpRequest, course_id: int, id: int) -> HttpRequest:
        try:
            course = Course.objects.get(id=course_id, creator=request.user)
            chapter = Chapter.objects.get(id=id, course=course)
        except (Course.DoesNotExist, Chapter.DoesNotExist):
            return redirect('course_details', course_id)

        form = ChapterForm(request.POST, instance=chapter)

        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully edited chapter.')
            return redirect('course_details', course.pk)
        else:
            messages.error(request, 'Invalid data.')
            return self.get(request, course.pk, chapter.pk)
