from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from platformaDoKursow.models import Course, Participant
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db.models import Count


@method_decorator(login_required, name='dispatch')
class CourseView(View):
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        custom_actions = {
            ('created_by_you', 'GET'): self.created_by_you,
            ('your_started', 'GET'): self.your_started_courses,
            ('delete', 'POST'): self.delete
        }


        if (action := custom_actions.get((kwargs.get('action'), request.method))):
            return action(request)

        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(
            request, 'course/get.html',
            {'courses': Course.objects.select_related('creator').filter(public=True)}
        )

    def delete(self, request: HttpRequest) -> HttpResponse:
        try:
            Course.objects.get(creator=request.user, id=request.GET.get('id')).delete()
        except Course.DoesNotExist:
            messages.error('Course not found')
        return self.created_by_you(request)

    def created_by_you(self, request: HttpRequest) -> HttpResponse:
        return render(
            request, 'course/created_by_you.html',
            {'courses': Course.objects.filter(creator=request.user).annotate(
                chapters_count=Count('chapters')
            )}
        )

    def your_started_courses(self, request: HttpRequest) -> HttpResponse:
        return render(
            request, 'course/your_started.html',
            {'courses': Participant.objects.filter(user=request.user).select_related('course')}
        )
