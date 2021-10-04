from django.urls import path
from . import views
urlpatterns = [
    path('student/signup', views.signupTeacher, name='teacherSignup'),
    path('teacher/signup/', views.signupStudent, name='studentSignup'),
    path('signin/', views.signin, name='signin'),

    path('student/dashboard/', views.studentDashboard, name='studentDashboard'),
    path('teacher/dashboard/', views.teacherDashboard, name='teacherDashboard'),

    path('logout/', views.signout, name='signout')

]