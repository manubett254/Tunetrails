from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, TeacherProfileForm
from .models import TeacherProfile, User
from django.http import HttpResponse
from django.contrib import messages


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.is_teacher:
                return redirect('teacher_profile')  # teacher sets up profile next
            else:
                return redirect('student_dashboard')  # student sees list
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
                return redirect('teacher_dashboard')
            else:
                return redirect('student_dashboard')
        else:
            return render(request, 'core/login.html', {'error': 'Invalid credentials'})
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def home_view(request):
    return render(request, 'core/home.html')



@login_required
def student_dashboard(request):
    if request.user.is_teacher:
        return redirect('teacher_dashboard')
    return render(request, 'core/student_dashboard.html')


@login_required
def teacher_dashboard(request):
    if not request.user.is_teacher:
        return redirect('student_dashboard')
    try:
        request.user.teacherprofile
    except TeacherProfile.DoesNotExist:
        return redirect('teacher_profile')
    return render(request, 'core/teacher_dashboard.html')


@login_required
def teacher_profile_create(request):
    if not request.user.is_teacher:
        return redirect('student_dashboard')

    try:
        # If profile already exists, go to dashboard
        request.user.teacherprofile
        return redirect('teacher_dashboard')
    except TeacherProfile.DoesNotExist:
        pass

    if request.method == 'POST':
        form = TeacherProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('teacher_dashboard')
    else:
        form = TeacherProfileForm()
    return render(request, 'core/teacher_profile_form.html', {'form': form})

@login_required
def teacher_profile_view(request):
    if not request.user.is_teacher:
        return redirect('student_dashboard')

    try:
        profile = request.user.teacherprofile
    except TeacherProfile.DoesNotExist:
        return redirect('teacher_profile')  # redirect to form if no profile
    
    instruments = profile.instruments_taught.split(', ')
    return render(request, 'core/teacher_profile_view.html', {
        'profile': profile,
        'instruments': instruments,
    })

@login_required
def teacher_list(request):
    if request.user.is_teacher:
        return redirect('teacher_dashboard')

    teachers = TeacherProfile.objects.all()
    return render(request, 'core/teacher_list.html', {'teachers': teachers})

@login_required
def teacher_profile_edit(request):
    if not request.user.is_teacher:
        return redirect('student_dashboard')

    try:
        profile = request.user.teacherprofile
    except TeacherProfile.DoesNotExist:
        return redirect('teacher_profile')

    if request.method == 'POST':
        form = TeacherProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('teacher_profile_view')
    else:
        form = TeacherProfileForm(instance=profile)

    return render(request, 'core/teacher_profile_form.html', {'form': form, 'edit_mode': True})


@login_required
def teacher_profile_delete(request):
    if not request.user.is_teacher:
        return redirect('student_dashboard')

    try:
        profile = request.user.teacherprofile
        profile.delete()
        return redirect('teacher_dashboard')
    except TeacherProfile.DoesNotExist:
        return redirect('teacher_dashboard')

@login_required
def teacher_detail(request, teacher_id):
    try:
        teacher = TeacherProfile.objects.get(id=teacher_id)
    except TeacherProfile.DoesNotExist:
        return redirect('teacher_list')

    return render(request, 'core/teacher_detail.html', {'teacher': teacher})
