from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from platformaDoKursow.views.test_view import test
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
from platformaDoKursow.views.chapter.remove_chapter_view import RemoveChapterView
from platformaDoKursow.views.quiz.manage_quiz_view import ManageQuizView
from platformaDoKursow.views.chapter.upload_image_view import custom_ckeditor_upload
from platformaDoKursow.views.course.remove_user_from_course_view import RemoveUserFromCourseView
from platformaDoKursow.views.quiz.solve_quiz_view import SolveQuizView
from django.conf import settings
from platformaDoKursow.views.quiz.quiz_attempts_view import QuizAttemptsView
from platformaDoKursow.views.training.training_view import TrainingView
from platformaDoKursow.views.training.schedule_training_view import ScheduleTrainingView
from platformaDoKursow.views.training.join_training_view import JoinTrainingView
from platformaDoKursow.views.course.join_new_course_view import JoinNewCourseView


urlpatterns = [
    path('admin', admin.site.urls),
    path('', test, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register', registration_view, name='register'),
    path('accounts/login/', login_redirect, name='redirect'),

    path('courses', CourseView.as_view(), name='courses'),
    path('courses/create', CreateCourseView.as_view(), name='create_course'),
    path('courses/<int:id>/details', CourseDetailsView.as_view(), name='course_details'),
    path('courses/<int:id>/edit', CourseEditView.as_view(), name='edit_course'),
    path('courses/<int:id>/generate_invitation_token', GenerateInvitationTokenView.as_view(), name='generate_invititation_token'),
    path('courses/join', JoinCourseView.as_view(), name='join_course'),
    path('courses/join/<int:id>', JoinNewCourseView.as_view(), name='join_new_course'),
    path('courses/leave', LeaveCourseView.as_view(), name='leave_course'),
    path('courses/<int:id>/remove_user_from_course', RemoveUserFromCourseView.as_view(), name='remove_user_from_course'),

    path('courses/<int:course_id>/chapters/create', CreateChapterView.as_view(), name='create_chapter'),
    path('courses/<int:course_id>/chapters/<int:id>', ChapterView.as_view(), name='chapter'),
    path('courses/<int:course_id>/chapters/<int:id>/remove', RemoveChapterView.as_view(), name='remove_chapter'),

    path('courses/<int:course_id>/chapters/<int:chapter_id>/quiz', ManageQuizView.as_view(), name='manage_quiz'),

    path('course/<int:id>', ShowCourseView.as_view(), name='show_course'),
    path('course/<int:course_id>/chapter/<int:chapter_id>/quiz', SolveQuizView.as_view(), name='solve_quiz'),
    path('course/<int:course_id>/chapter/<int:chapter_id>/quiz_attempts', QuizAttemptsView.as_view(), name='quiz_attempts'),

    path('courses/<str:action>', CourseView.as_view(), name='other_courses'),
    path('ckeditor/upload/', custom_ckeditor_upload, name='ckeditor_upload'),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('trainings', TrainingView.as_view(), name='trainings'),
    path('trainings/new', ScheduleTrainingView.as_view(), name='schedule_training'),
    path('trainings/<int:id>/join', JoinTrainingView.as_view(), name='join_training'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
