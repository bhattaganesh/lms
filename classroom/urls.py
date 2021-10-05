from django.urls import path
from . import views
urlpatterns = [
    path('create-class/', views.createClassroom, name='createClassroom'),
    path('search-class/', views.classSearch, name='classSearch'),
]