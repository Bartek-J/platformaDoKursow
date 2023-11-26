from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Course(models.Model):
    class Meta:
        db_table = 'courses'

    name = models.CharField(blank=False, null=False, max_length=255)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=True)
    invitation_token = models.CharField(null=True, max_length=255)


class Chapter(models.Model):
    class Meta:
        db_table = 'chapters'

    title = models.CharField(null=False, blank=False, max_length=255)
    content = RichTextField(null=False, blank=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='chapters')


class Quiz(models.Model):
    class Meta:
        db_table = 'quizes'

    title = models.CharField(null=False, blank=False, max_length=255)
    description = models.TextField(null=True, blank=False)
    chapter = models.OneToOneField(Chapter, on_delete=models.CASCADE)
    percentage_required = models.FloatField(default=0.5)
    allowed_attempts = models.IntegerField(default=1)


class Question(models.Model):
    class Meta:
        db_table = 'questions'

    text = models.TextField(null=False, blank=False)
    type = models.CharField(null=False, blank=False, max_length=255)
    points = models.IntegerField(null=False, blank=False)
    partially_accepted = models.BooleanField(blank=False, null=False, default=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Answer(models.Model):
    class Meta:
        db_table = 'answers'

    text = models.CharField(null=False, blank=False, max_length=255)
    is_correct = models.BooleanField(null=False, blank=False, default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Participant(models.Model):
    class Meta:
        db_table = 'participants'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='participants')
    progress = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class QuizAttempt(models.Model):
    class Meta:
        db_table = 'quiz_attempts'
        unique_together = ('user_id', 'course_id')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    points = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
