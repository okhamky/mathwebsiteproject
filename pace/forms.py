from django import forms
from .models import User, Student, Book, Chapter, PaceChapter


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class AddStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['teacher', 'user']


class AddBookToStudentForm(forms.Form):
    book = forms.ModelChoiceField(Book.objects.all(), widget=forms.RadioSelect, empty_label=None)


class AddChapterToStudentForm(forms.Form):
    chapter = forms.ModelMultipleChoiceField(Chapter.objects.all(), widget=forms.CheckboxSelectMultiple)


class DeleteChapterForm(forms.Form):
    chapter = forms.ModelMultipleChoiceField(PaceChapter.objects.all(), widget=forms.CheckboxSelectMultiple)


class EditPaceDatesForm(forms.ModelForm):
    chapter = forms.ModelChoiceField(Chapter.objects.all(), disabled=True)

    class Meta:
        model = PaceChapter
        fields = ['chapter', 'pace_date']