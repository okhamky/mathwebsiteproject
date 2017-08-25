from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch
from .models import PaceChapter, Student
from datetime import date
from itertools import chain

def index(request):
    return render(request, 'pace/index.html')


def whereto(request):
    if request.user.groups.filter(name='Student').exists():
        return redirect('pace:pacechart')
    elif request.user.groups.filter(name='Teacher').exists():
        return redirect('/teacher/' + str(request.user.username))
    else:
        return HttpResponse("You are not a teacher or a student. Whoops! Let someone know and we will fix it")


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
    teacher_students = Student.objects.prefetch_related('teacher').all()
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


