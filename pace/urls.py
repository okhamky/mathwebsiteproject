from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'pace'
urlpatterns = [
    url(r'^$', auth_views.LoginView.as_view()),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^whereto/', views.whereto, name='whereto'),
    url(r'^pacechart/', views.pacechart, name='pacechart'),
    url(r'^teacher/(?P<teacher_name>[a-zA-Z0-9 ]+)/$', views.teacher, name='teacher'),
    url(r'^teacher/(?P<teacher_name>[a-zA-Z0-9 ]+)/addstudent/$', views.addstudent, name='addstudent'),
    url(r'^teacher/(?P<teacher_name>[a-zA-Z0-9 ]+)/(?P<student_name>[a-zA-Z0-9 ]+)/$', views.teacher, name='teacher'),
    url(
        r'^teacher/(?P<teacher_name>[a-zA-Z0-9 ]+)/(?P<student_name>[a-zA-Z0-9 ]+)/add_book/$',
        views.add_book_to_student,
        name='add_book_to_student'
    ),
    url(
        r'^teacher/(?P<teacher_name>[a-zA-Z0-9 ]+)/(?P<student_name>[a-zA-Z0-9 ]+)/add_chapter/$',
        views.add_chapter_to_student,
        name='add_chapter_to_student'
    ),
    url(
        r'^teacher/(?P<teacher_name>[a-zA-Z0-9 ]+)/(?P<student_name>[a-zA-Z0-9 ]+)/delete_chapter/$',
        views.delete_chapter,
        name='delete_chapter'
    ),
    url(
        r'^teacher/(?P<teacher_name>[a-zA-Z0-9 ]+)/(?P<student_name>[a-zA-Z0-9 ]+)/delete_selected_chapter/$',
        views.delete_selected_chapter,
        name='delete_selected_chapter'
    ),
    url(
        r'^teacher/(?P<teacher_name>[a-zA-Z0-9 ]+)/(?P<student_name>[a-zA-Z0-9 ]+)/edit_pace_dates/$',
        views.edit_pace_dates,
        name='edit_pace_dates'
    ),
    url(
        r'^teacher/(?P<teacher_name>[a-zA-Z0-9 ]+)/(?P<student_name>[a-zA-Z0-9 ]+)/save_pace_dates/$',
        views.save_pace_dates,
        name='save_pace_dates'
    ),
    url(
        r'^teacher/(?P<teacher_name>[a-zA-Z0-9 ]+)/(?P<student_name>[a-zA-Z0-9 ]+)/(?P<pacechapter>[a-zA-Z0-9 ]+)/edit_grade/$',
        views.edit_grade,
        name='edit_grade'
    ),
    url(
        r'^teacher/(?P<teacher_name>[a-zA-Z0-9 ]+)/(?P<student_name>[a-zA-Z0-9 ]+)/(?P<chosen_book>[a-zA-Z0-9 ]+)/add_selected_chapters/$',
        views.add_selected_chapters,
        name='add_selected_chapters'
    ),
]