from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from platformaDoKursow.views import test_view
from platformaDoKursow.views.login_view import login_view, logout_view, registration_view, login_redirect
from platformaDoKursow.views.course.course_view import CourseView
from platformaDoKursow.views.course.course_edit_view import CourseEditView
from platformaDoKursow.views.course.join_course_view import JoinCourseView
from platformaDoKursow.views.course.show_course_view import ShowCourseView
from platformaDoKursow.views.course.leave_course_view import LeaveCourseView
from platformaDoKursow.views.course.create_course_view import CreateCourseView
from platformaDoKursow.views.course.course_details_view import CourseDetailsView
from platformaDoKursow.views.course.generate_invitation_token_view import GenerateInvitationTokenView
from platformaDoKursow.views.chapter.chapter_view import ChapterView
from platformaDoKursow.views.chapter.create_chapter_view import CreateChapterView
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', test_view.test, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', registration_view, name='register'),
    path('accounts/login/', login_redirect, name='redirect'),

    path('courses', CourseView.as_view(), name='courses'),
    path('courses/create', CreateCourseView.as_view(), name='create_course'),
    path('courses/<int:id>/details', CourseDetailsView.as_view(), name='course_details'),
    path('courses/<int:id>/edit', CourseEditView.as_view(), name='edit_course'),
    path('courses/<int:id>/generate_invitation_token', GenerateInvitationTokenView.as_view(), name='generate_invititation_token'),
    path('courses/join', JoinCourseView.as_view(), name='join_course'),
    path('courses/leave', LeaveCourseView.as_view(), name='leave_course'),

    path('courses/<int:course_id>/chapters/create', CreateChapterView.as_view(), name='create_chapter'),
    path('courses/<int:course_id>/chapters/<int:id>', ChapterView.as_view(), name='chapter'),

    # path('courses/<int:id>/chapters/<int:id>/quiz'),

    path('course/<int:id>', ShowCourseView.as_view(), name='show_course'),


    path('courses/<str:action>', CourseView.as_view(), name='other_courses'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

### Chapters
# add chapter
# edit chapter
# remove chapter
## quiz
# enable/disable quiz
# add question
# remove question
# edit question

### Completing course
# enter course
# select chapter
# complete quiz
# course progress