from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from platformaDoKursow.models import Course
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class CourseDetailsView(View):
    def get(self, request: HttpRequest, id: int) -> HttpResponse:
        try:
            course = Course.objects.prefetch_related(
                'chapters', 'participants', 'participants__user'
            ).get(id=id)
        except Course.DoesNotExist:
            messages.error(request, 'Course not found.')
            return redirect('courses')

        return render(
            request, 'course/details.html',
            {'course': course, }
        )
