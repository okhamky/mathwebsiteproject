from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch
from .models import PaceChapter, Student, Teacher, Chapter
from datetime import date
from itertools import chain
from django.forms import modelformset_factory
from .forms import AddStudentForm, UserForm, AddBookToStudentForm, AddChapterToStudentForm, DeleteChapterForm, \
    EditPaceDatesForm, EditGradeForm

def index(request):
    return render(request, 'pace/index.html')


def whereto(request):
    if request.user.groups.filter(name='Student').exists():
        return redirect('pace:pacechart')
    elif request.user.groups.filter(name='Teacher').exists():
        return redirect('/teacher/' + str(request.user.username))
    else:
        return redirect('pace:pacechart')


def is_teacher(user):
    if user.groups.filter(name='Teacher').exists():
        return True
    else:
        return False


@login_required
def pacechart(request, user=None):
    if not user:
        user = request.user
    all_chapters = PaceChapter.objects.select_related('student__user').filter(student__user=user)
    all_chapters_not_null = all_chapters.filter(pace_date__isnull=False)
    all_chapters_null = all_chapters.filter(pace_date__isnull=True).order_by('complete_date', 'chapter__chapter_number')
    all_chapters = list(chain(all_chapters_not_null,all_chapters_null))
    return render(request, 'pace/pacechart.html', {'all_chapters': all_chapters, 'date_today': date.today()})


@login_required
@user_passes_test(is_teacher)
def teacher(request, teacher_name, student_name=None):
    teacher_students = Student.objects.filter(teacher__user__username=teacher_name)
    if student_name:
        student_chapters = PaceChapter.objects.prefetch_related('student__user').filter(student__user__username=student_name)
        student_chapters_not_null = student_chapters.filter(pace_date__isnull=False)
        student_chapters_null = student_chapters.filter(pace_date__isnull=True).order_by('complete_date', 'chapter__chapter_number')
        student_chapters = list(chain(student_chapters_not_null, student_chapters_null))
    else:
        student_chapters = None
    context = {
        'teacher_name': teacher_name,
        'student_name': student_name,
        'teacher_students': teacher_students,
        'student_chapters': student_chapters,
        'date_today': date.today()
            }
    return render(request, 'pace/teacher.html', context)


@login_required
@user_passes_test(is_teacher)
def addstudent(request, teacher_name=None):
    if request.method == 'POST':
        student_form = AddStudentForm(request.POST)
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            new_student = student_form.save(commit=False)
            new_student.user = user_form.save()
            if student_form.is_valid():
                comment = 'Success! Student added.'
                student_form.save()
            else:
                comment = 'Please correct the errors below. (SF)'
        else:
            comment = 'Please correct the errors below. (UF)'
    else:
        student_form = AddStudentForm(initial={'teacher': Teacher.objects.filter(user__username=teacher_name)})
        user_form = UserForm()
        comment = None

    context = {
        'teacher_name': teacher_name,
        'student_form': student_form,
        'user_form': user_form,
        'top_comment': comment,
            }
    return render(request, 'pace/addstudent.html', context)


@login_required
@user_passes_test(is_teacher)
def add_book_to_student(request, teacher_name=None, student_name=None):
    if request.method == 'POST':
        form = AddBookToStudentForm()
        comment = None
        context = {
            'teacher_name': teacher_name,
            'student_name': student_name,
            'form': form,
            'top_comment': comment,
        }
        return render(request, 'pace/addbooktostudent.html', context)
    else:
        return redirect('pace:whereto')


@login_required
@user_passes_test(is_teacher)
def add_chapter_to_student(request, teacher_name, student_name):
    if request.method == 'POST':
        book_form = AddBookToStudentForm(request.POST)
        if book_form.is_valid():
            data = book_form.cleaned_data
            chosen_book = data['book']
            chapter_form = AddChapterToStudentForm()
            chapter_form.fields["chapter"].queryset = Chapter.objects.filter(book__book_name=chosen_book)
        else:
            return HttpResponse('book choice error')
        comment = None
        context = {
            'teacher_name': teacher_name,
            'student_name': student_name,
            'chosen_book': str(chosen_book),
            'form': chapter_form,
            'top_comment': comment,
        }
        return render(request, 'pace/addchaptertostudent.html', context)
    else:
        return redirect('pace:whereto')


@login_required
@user_passes_test(is_teacher)
def add_selected_chapters(request, teacher_name, student_name, chosen_book):
    if request.method == 'POST':
        chapters_form = AddChapterToStudentForm(request.POST)
        if chapters_form.is_valid():
            data = chapters_form.cleaned_data
            chosen_chapters = data['chapter'].values()
            for chapter in chosen_chapters:
                chapter_number = chapter['chapter_number']
                PaceChapter.objects.create(
                    student=Student.objects.filter(user__username=student_name).first(),
                    chapter=Chapter.objects.filter(book__book_name=chosen_book, chapter_number=chapter_number).first()
                )
            return redirect('pace:teacher', teacher_name, student_name)
        else:
            return redirect('pace:teacher', teacher_name, student_name)
    else:
        return redirect('pace:whereto')


@login_required
@user_passes_test(is_teacher)
def delete_chapter(request, teacher_name, student_name):
    if request.method == 'POST':
        form = DeleteChapterForm()
        form.fields["chapter"].queryset = PaceChapter.objects.filter(student__user__username=student_name)
        comment = None
        context = {
            'teacher_name': teacher_name,
            'student_name': student_name,
            'form': form,
            'top_comment': comment,
        }
        return render(request, 'pace/deletechapter.html', context)
    else:
        return redirect('pace:teacher', teacher_name, student_name)

@login_required
@user_passes_test(is_teacher)
def delete_selected_chapter(request, teacher_name, student_name):
    if request.method == 'POST':
        selected_chapters_form = DeleteChapterForm(request.POST)
        if selected_chapters_form.is_valid():
            selected_chapters = selected_chapters_form.cleaned_data["chapter"]
            for pacechapter in selected_chapters:
                target = pacechapter
                target.delete()
            return redirect('pace:teacher', teacher_name, student_name)
        else:
            return HttpResponse('deletion error')
    else:
        return redirect('pace:teacher', teacher_name, student_name)


@login_required
@user_passes_test(is_teacher)
def edit_pace_dates(request, teacher_name, student_name):
    if request.method == 'POST':
        formset = modelformset_factory(PaceChapter, form=EditPaceDatesForm, fields=('chapter', 'pace_date',), extra=0)
        formset = formset(queryset=PaceChapter.objects.filter(student__user__username=student_name).order_by('pace_date', 'chapter__book', 'chapter__chapter_number'))
        comment = None
        context = {
            'teacher_name': teacher_name,
            'student_name': student_name,
            'form': formset,
            'top_comment': comment,
        }
        return render(request, 'pace/editpacedates.html', context)
    else:
        return redirect('pace:teacher', teacher_name, student_name)

@login_required
@user_passes_test(is_teacher)
def save_pace_dates(request, teacher_name, student_name):
    if request.method == 'POST':
        formset = modelformset_factory(PaceChapter, form=EditPaceDatesForm, fields=('chapter', 'pace_date',), extra=0)
        form = formset(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pace:teacher', teacher_name, student_name)
        else:
            comment = "Please correct the errors below"
            context = {
                'teacher_name': teacher_name,
                'student_name': student_name,
                'form': form,
                'top_comment': comment,
            }
            return render(request, 'pace/editpacedates.html', context)
    else:
        return redirect('pace:teacher', teacher_name, student_name)


@login_required
@user_passes_test(is_teacher)
def edit_grade(request, teacher_name, student_name, pacechapter):
    if request.method == 'POST':
        try:
            chapter_instance = PaceChapter.objects.get(pk=pacechapter)
        except:
            return redirect('pace:teacher', teacher_name, student_name)
        form = EditGradeForm(request.POST, instance=chapter_instance)
        if form.is_valid():
            form.save()
            return redirect('pace:teacher', teacher_name, student_name)
        else:
            comment = "Please correct the errors below"
            context = {
                'teacher_name': teacher_name,
                'student_name': student_name,
                'pacechapter': pacechapter,
                'form': form,
                'top_comment': comment,
            }
            return render(request, 'pace/editscore.html', context)
    else:
        try:
            chapter_instance = PaceChapter.objects.get(pk=pacechapter)
        except:
            return redirect('pace:teacher', teacher_name, student_name)
        if chapter_instance.student.user.username == student_name:
            form = EditGradeForm(instance=chapter_instance)
            if not form.initial['complete_date']:
                form.initial['complete_date'] = date.today()
            comment = None
            context = {
                'teacher_name': teacher_name,
                'student_name': student_name,
                'pacechapter': pacechapter,
                'form': form,
                'top_comment': comment,
            }
            return render(request, 'pace/editscore.html', context)
        else:
            return redirect('pace:teacher', teacher_name, student_name)