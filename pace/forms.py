from django import forms
from .models import User, Student


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class AddStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['teacher', 'user']

