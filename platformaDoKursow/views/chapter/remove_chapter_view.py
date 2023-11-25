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
class RemoveChapterView(View):
    def post(self, request: HttpRequest, course_id: int, id: int) -> HttpResponse:
        try:
            course = Course.objects.get(pk=course_id, creator=request.user)
            Chapter.objects.get(course_id=course_id, pk=id).delete()
        except (Course.DoesNotExist, Chapter.DoesNotExist):
            messages.error(request, 'Something went wrong.')
            return redirect('course_details', course.pk)

        messages.success(request, 'Successfully removed chapter.')
        return redirect('course_details', course.pk)
