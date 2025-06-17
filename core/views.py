from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, TeacherProfileForm
from .models import TeacherProfile, User
from django.http import HttpResponse

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.is_teacher:
                return redirect('teacher_profile')  # teacher sets up profile next
            else:
                return redirect('teacher_list')  # student sees list
    else:
        form = UserRegisterForm()
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.is_teacher:
                return redirect('teacher_profile')
            else:
                return redirect('teacher_list')
        else:
            return render(request, 'core/login.html', {'error': 'Invalid credentials'})
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def teacher_profile_create(request):
    if not request.user.is_teacher:
        return redirect('teacher_list')

    try:
        profile = request.user.teacherprofile
        return redirect('teacher_list')  # profile exists already
    except TeacherProfile.DoesNotExist:
        pass

    if request.method == 'POST':
        form = TeacherProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('teacher_list')
    else:
        form = TeacherProfileForm()
    return render(request, 'core/teacher_profile_form.html', {'form': form})



def teacher_list(request):
    return HttpResponse("Teacher list will go here.")

def home_redirect(request):
    return redirect('login')  # or 'register' if you prefer

def home_view(request):
    return render(request, 'core/home.html')
