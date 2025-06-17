from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('teacher/profile/', views.teacher_profile_create, name='teacher_profile'),
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('', views.home_view, name='home'),

]
