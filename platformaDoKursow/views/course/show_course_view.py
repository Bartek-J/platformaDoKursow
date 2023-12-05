from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from platformaDoKursow.models import Course, QuizAttempt
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class ShowCourseView(View):
    def get(self, request: HttpRequest, id: int) -> HttpResponse:
        try:
            course = Course.objects.prefetch_related('chapters', 'chapters__quiz').get(id=id)
        except Course.DoesNotExist:
            messages.error(request, 'Course not found.')
            return redirect('courses')

        passed_quizes = [
            succesful_attempt.quiz_id
            for succesful_attempt in QuizAttempt.objects.filter(user=request.user, course=course, quiz_passed=True)
        ]

        return render(
            request, 'course/show.html',
            {'course': course, 'passed_quizes': passed_quizes}
        )
