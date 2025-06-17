from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
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




]
