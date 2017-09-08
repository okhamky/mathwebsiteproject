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
]