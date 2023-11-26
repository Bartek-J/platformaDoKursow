from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from platformaDoKursow.forms.course_form import CourseForm
from platformaDoKursow.models import Course, Participant, Chapter
from django.utils.decorators import method_decorator
from platformaDoKursow.forms.chapter_form import ChapterForm
from platformaDoKursow.helpers.quiz_validator import QuizValidator
from json import loads


@method_decorator(login_required, name='dispatch')
class ManageQuizView(View):
    def get(self, request: HttpRequest, course_id: int, chapter_id: int) -> HttpResponse:
        try:
            chapter = Chapter.objects.get(id=chapter_id, course_id=course_id, course__creator=request.user)
        except Chapter.DoesNotExist:
            messages.error('Chapter not found.')
            return redirect('course_details', course_id)
        return render(
            request, 'quiz/manage_quiz.html',
            {'chapter': chapter}
        )

    def post(self, request: HttpRequest, course_id: int, chapter_id: int) -> HttpRequest:
        try:
            chapter = Chapter.objects.get(id=chapter_id, course_id=course_id, course__creator=request.user)
        except Chapter.DoesNotExist:
            return JsonResponse(data={'errors': 'Chapter not found.'}, status=400)

        request_data = QuizValidator(loads(request.body), chapter)
        if request_data.is_valid():
            request_data.save()
            return JsonResponse(data={'message': 'success'})
        return JsonResponse(data={'errors': list(request_data.errors)}, status=400)
