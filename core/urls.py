from django.urls import path
from . import views

urlpatterns = [
    # urls.py
    path('register/student/', views.register_student_view, name='register_student'),
    path('register/teacher/', views.register_teacher_view, name='register_teacher'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('teacher/profile/', views.teacher_profile_create, name='teacher_profile'),
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('', views.home_view, name='home'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/profile/', views.teacher_profile_create, name='teacher_profile'),
    path('teacher/profile/view/', views.teacher_profile_view, name='teacher_profile_view'),
    path('teacher/profile/edit/', views.teacher_profile_edit, name='teacher_profile_edit'),
    path('teacher/profile/delete/', views.teacher_profile_delete, name='teacher_profile_delete'),
    path('teachers/<int:teacher_id>/', views.teacher_detail, name='teacher_detail'),
    path('lessons/request/<int:teacher_id>/', views.request_lesson, name='request_lesson'),
    path('lessons/<int:lesson_id>/approve/', views.approve_lesson, name='approve_lesson'),
    path('lessons/<int:lesson_id>/decline/', views.decline_lesson, name='decline_lesson'),
    path('lessons/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('lessons/<int:lesson_id>/cancel/', views.cancel_lesson_student, name='cancel_lesson'),
    path('lessons/<int:lesson_id>/cancel/teacher/', views.cancel_lesson_teacher, name='cancel_lesson_teacher'),
    path('lessons/<int:lesson_id>/cancel/student/', views.cancel_lesson_student, name='cancel_lesson_student'),
    path('lessons/<int:lesson_id>/reschedule/', views.reschedule_lesson, name='reschedule_lesson'),
    path('lessons/<int:lesson_id>/reschedule/approve/', views.approve_reschedule, name='approve_reschedule'),
    path('lessons/<int:lesson_id>/reschedule/decline/', views.decline_reschedule, name='decline_reschedule'),









]
