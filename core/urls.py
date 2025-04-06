from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('courses/add/', views.add_course, name='add_course'),
    path('modules/add/', views.add_module, name='add_module'),
    path('lessons/add/', views.add_lesson, name='add_lesson'),
    path('courses/', views.course_list, name='course_list'),
    path('lessons/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('register/', views.register, name='register'),
    path('lessons/<int:lesson_id>/complete/', views.complete_lesson, name='complete_lesson'),
    path('profile/', views.profile, name='profile'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('modules/<int:module_id>/complete/', views.complete_module, name='complete_module'),
    path('modules/<int:module_id>/uncomplete/', views.uncomplete_module, name='uncomplete_module'),
    path('modules/<int:module_id>/', views.module_detail, name='module_detail'),
]
