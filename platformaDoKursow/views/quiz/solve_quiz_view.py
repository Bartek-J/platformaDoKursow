from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from platformaDoKursow.models import Course, Quiz, QuizAttempt
from django.utils.decorators import method_decorator
from platformaDoKursow.helpers.solve_quiz_service import SolveQuizService, SolveQuizServiceError
from json import loads


@method_decorator(login_required, name='dispatch')
class SolveQuizView(View):
    def get(self, request: HttpRequest, course_id: int, chapter_id: int) -> HttpResponse:
        try:
            course = Course.objects.get(
                participants__user=request.user,
                id=course_id
            )
            quiz = Quiz.objects.prefetch_related('questions', 'questions__answers').get(
                chapter_id=chapter_id,
                chapter__course=course,
            )
        except (Quiz.DoesNotExist, Course.DoesNotExist):
            messages.error(request, 'Quiz not found.')
            return redirect('show_course', course_id)

        if quiz.allowed_attempts and \
            QuizAttempt.objects.filter(user=request.user, quiz=quiz).count() == quiz.allowed_attempts:
            messages.error(request, 'You don\'t have any quiz attempts left.')
            return redirect('show_course', course_id)

        return render(
            request, 'quiz/solve.html',
            {'quiz': quiz, 'course_id': course_id, 'chapter_id': chapter_id }
        )

    def post(self, request: HttpRequest, course_id: int, chapter_id: int) -> HttpResponse:
        try:
            course = Course.objects.get(
                participants__user=request.user,
                id=course_id
            )
            quiz = Quiz.objects.prefetch_related('questions', 'questions__answers').get(
                chapter_id=chapter_id,
                chapter__course=course,
            )
        except (Quiz.DoesNotExist, Course.DoesNotExist):
            messages.error(request, 'Quiz not found.')
            return JsonResponse(data={'errors': 'Quiz not found.'}, status=400)

        try:
            SolveQuizService(
                quiz=quiz, user=request.user, course=course, request_data=loads(request.body)
            ).run()
        except SolveQuizServiceError as e:
            messages.error(request, str(e))
            return JsonResponse(data={'errors': str(e)}, status=400)

        messages.success(request, 'Quiz attempt was saved.')
        return JsonResponse(data={'message': 'success'}, status=200)
