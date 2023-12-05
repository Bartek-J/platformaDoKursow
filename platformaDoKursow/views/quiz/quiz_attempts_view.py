from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from platformaDoKursow.forms.course_form import CourseForm
from platformaDoKursow.models import Course, Participant, Chapter, QuizAttempt, Quiz
from django.utils.decorators import method_decorator
from platformaDoKursow.forms.chapter_form import ChapterForm
from platformaDoKursow.helpers.quiz_validator import QuizValidator
from json import loads


@method_decorator(login_required, name='dispatch')
class QuizAttemptsView(View):
    def get(self, request: HttpRequest, course_id: int, chapter_id: int) -> HttpResponse:
        try:
            chapter = Chapter.objects.select_related('course', 'quiz').get(id=chapter_id, course_id=course_id)
        except Chapter.DoesNotExist:
            messages.error(request, 'Chapter not found.')
            return redirect('show_course', course_id)

        quiz_attempts = QuizAttempt.objects.filter(quiz=chapter.quiz, user=request.user)
        quiz_passed = any(attempt.quiz_passed for attempt in quiz_attempts)
        return render(
            request, 'quiz/attempts.html',
            {
                'chapter': chapter, 'quiz_attempts': quiz_attempts, 'quiz_passed': quiz_passed,
                'chapter_id': chapter_id, 'course_id': course_id
            }
        )
