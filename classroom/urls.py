from django.urls import path
from . import views
urlpatterns = [
    path('create-class/', views.createClassroom, name='createClassroom'),
    path('search-class/', views.classSearch, name='classSearch'),
    path('join-class/<int:id>/', views.classJoin, name='classJoin'),
    path('course-details/<int:id>/', views.courseDetails, name='courseDetails'),
    path('class-join-request-accept/<int:id>/', views.classroomJoinRequest, name='classJoinAccept'),
]