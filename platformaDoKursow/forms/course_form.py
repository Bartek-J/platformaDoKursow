from django import forms
from platformaDoKursow.models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description','public']
