from django.urls import path,include

from rest_framework.routers import DefaultRouter

from todoapi import views

urlpatterns = [
    path('welcome/', views.welcome),
    path('', views.welcome),
    path('todo/',views.todo),
    path('todoid/',views.todoid),
    path('signup/',views.signup),
    path('signin/',views.signin),
    path('assign/',views.assign),
    path('user/',views.getuser),
    path('useralltask/',views.userall)
]