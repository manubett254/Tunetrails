from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, TeacherProfileForm, LessonRequestForm , RescheduleLessonForm , LessonProgressForm,CourseForm, CourseLessonForm
from django.views.decorators.http import require_POST
from .models import TeacherProfile, Lesson ,Course, CourseLesson
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import Group
from django.core.mail import send_mail


def register_student_view(request):
    return _handle_register(request, is_teacher=False)

def register_teacher_view(request):
    return _handle_register(request, is_teacher=True)

def _handle_register(request, is_teacher):
    print(f"Handling register request, is_teacher={is_teacher}")  # Debug
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            print("Form is valid")  # Debug
            user = form.save(commit=False)
            user.is_teacher = is_teacher
            user.save()
            print(f"User created, is_teacher={user.is_teacher}")  # Debug
            if is_teacher:
                return redirect('teacher_profile')
            return redirect('student_dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'core/register.html', {
        'form': form,
        'is_teacher': is_teacher
    })

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

def handle_social_redirect(request):
    next_url = request.GET.get('next', '')

    if '/register/teacher/' in next_url:
        request.user.is_teacher = True
        request.user.save()  # Don't forget to save!
        return redirect('teacher_dashboard')

    if '/register/student/' in next_url:
        request.user.is_teacher = False
        request.user.save()  # Don't forget to save!
        return redirect('student_dashboard')

    return redirect('student_dashboard')

@login_required
def student_dashboard(request):
    if request.user.is_teacher:
        return redirect('teacher_dashboard')

    pending_lessons = Lesson.objects.filter(student=request.user, status='pending')
    approved_lessons = Lesson.objects.filter(student=request.user, status='approved')
    declined_lessons = Lesson.objects.filter(student=request.user, status='declined')
    cancelled_lessons = Lesson.objects.filter(
        student=request.user,
        status__in=['cancelled_by_student', 'cancelled_by_teacher']
    )
      # NEW: fetch enrolled courses
    enrolled_courses = Course.objects.filter(courseenrollment__user=request.user)



    return render(request, 'core/student_dashboard.html', {
        'pending_lessons': pending_lessons,
        'approved_lessons': approved_lessons,
        'declined_lessons': declined_lessons,
        'cancelled_lessons': cancelled_lessons,
        'assignments': [],  # placeholder
        'teachers': [],     # placeholder
        'enrolled_courses': enrolled_courses,
    })

@login_required
def teacher_dashboard(request):
    if not request.user.is_teacher:
        return redirect('student_dashboard')

    try:
        request.user.teacherprofile
    except TeacherProfile.DoesNotExist:
        return redirect('teacher_profile')

    approved_lessons = Lesson.objects.filter(teacher=request.user, status='approved').order_by('-date')
    pending_lessons = Lesson.objects.filter(teacher=request.user, status='pending').order_by('-date')
    declined_lessons = Lesson.objects.filter(teacher=request.user, status='declined').order_by('-date')
    cancelled_lessons = Lesson.objects.filter(
        teacher=request.user,
        status__in=['cancelled_by_student', 'cancelled_by_teacher']
    ).order_by('-date')

    # 🆕 Fetch courses
    courses = Course.objects.filter(teacher=request.user).order_by('-created_at')

    return render(request, 'core/teacher_dashboard.html', {
        'approved_lessons': approved_lessons,
        'pending_lessons': pending_lessons,
        'declined_lessons': declined_lessons,
        'cancelled_lessons': cancelled_lessons,
        'courses': courses,  # pass to template
    })


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

@login_required
def request_lesson(request, teacher_id):
    if request.user.is_teacher:
        return redirect('teacher_dashboard')

    try:
        teacher = TeacherProfile.objects.get(id=teacher_id).user
    except TeacherProfile.DoesNotExist:
        return redirect('teacher_list')

    if request.method == 'POST':
        form = LessonRequestForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.teacher = teacher
            lesson.student = request.user
            lesson.save()

            # ✅ Send email to teacher
            send_mail(
                subject='New Lesson Request on TuneTrails',
                message=f'Hi {teacher.username},\n\nYou’ve received a new lesson request from {request.user.username}.\n\nLesson: {lesson.title}\nDescription: {lesson.description}\n\nPlease log in to your dashboard to respond.',
                from_email='noreply@tunetrails.com',
                recipient_list=[teacher.email],
                fail_silently=True
            )

            messages.success(request, "Lesson request sent.")
            return redirect('student_dashboard')
    else:
        form = LessonRequestForm()

    return render(request, 'core/request_lesson.html', {'form': form, 'teacher': teacher})


@login_required
def lesson_detail(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)

    # Security: Make sure user is the student or teacher of this lesson
    if request.user != lesson.student and request.user != lesson.teacher:
        return redirect('home')

    return render(request, 'core/lesson_detail.html', {'lesson': lesson})

@login_required
def approve_lesson(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    if request.user != lesson.teacher:
        return redirect('teacher_dashboard')

    lesson.status = 'approved'
    lesson.save()
    messages.success(request, "Lesson approved.")
    return redirect('teacher_dashboard')


@login_required
def decline_lesson(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    if request.user != lesson.teacher:
        return redirect('teacher_dashboard')

    lesson.status = 'declined'
    lesson.save()
    messages.info(request, "Lesson declined.")
    return redirect('teacher_dashboard')


@login_required
def cancel_lesson_student(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)

    if lesson.student != request.user:
        return redirect('student_dashboard')

    if lesson.status == 'pending':
        lesson.status = 'cancelled_by_student'
        messages.success(request, "Lesson request cancelled.")
    elif lesson.status == 'approved':
        lesson.status = 'cancelled_by_student'
        messages.success(request, "Lesson cancelled. You may reschedule or pick another teacher.")
    else:
        messages.error(request, "You can't cancel this lesson.")
        return redirect('student_dashboard')

    lesson.save()
    # TODO: Notify teacher
    return redirect('student_dashboard')

@login_required
def cancel_lesson_teacher(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)

    if lesson.teacher != request.user:
        return redirect('teacher_dashboard')

    if lesson.status == 'approved':
        lesson.status = 'cancelled_by_teacher'
        messages.info(request, "You cancelled this lesson.")
        # TODO: Notify student
    else:
        messages.error(request, "Only approved lessons can be cancelled.")
        return redirect('teacher_dashboard')

    lesson.save()
    return redirect('teacher_dashboard')



@login_required
def reschedule_lesson(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)

    # Only student or teacher can request reschedule
    if request.user != lesson.student and request.user != lesson.teacher:
        return redirect('home')

    if request.method == 'POST':
        form = RescheduleLessonForm(request.POST, instance=lesson)
        if form.is_valid():
            updated = form.save(commit=False)
            updated.status = 'reschedule_requested'
            updated.reschedule_requested_by = request.user
            updated.save()
            messages.info(request, "Reschedule request submitted.")
            return redirect('lesson_detail', lesson_id=lesson.id)
    else:
        form = RescheduleLessonForm(instance=lesson)

    return render(request, 'core/reschedule_lesson.html', {'form': form, 'lesson': lesson})


@require_POST
@login_required
def approve_reschedule(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    if request.user != lesson.teacher:
        return redirect('home')

    lesson.date = lesson.new_date
    lesson.time = lesson.new_time
    lesson.status = 'approved'
    lesson.new_date = None
    lesson.new_time = None
    lesson.reschedule_requested_by = None
    lesson.save()
    messages.success(request, "Reschedule approved and updated.")
    return redirect('lesson_detail', lesson_id=lesson.id)


@require_POST
@login_required
def decline_reschedule(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    if request.user != lesson.teacher:
        return redirect('home')

    lesson.status = 'approved'
    lesson.new_date = None
    lesson.new_time = None
    lesson.reschedule_requested_by = None
    lesson.save()
    messages.info(request, "Reschedule request declined.")
    return redirect('lesson_detail', lesson_id=lesson.id)


@login_required
def teacher_students_view(request):
    if not request.user.is_teacher:
        return redirect('student_dashboard')
    
    lessons = Lesson.objects.filter(teacher=request.user, status='approved')
    students = set(lesson.student for lesson in lessons)
    
    return render(request, 'core/teacher_students.html', {'students': students})


@login_required
def add_progress_note(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)

    if request.user != lesson.teacher:
        return redirect('teacher_dashboard')

    if request.method == 'POST':
        form = LessonProgressForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            messages.success(request, "Progress note saved.")
            return redirect('lesson_detail', lesson_id=lesson.id)
    else:
        form = LessonProgressForm(instance=lesson)

    return render(request, 'core/add_progress_note.html', {'form': form, 'lesson': lesson})


@login_required
def upload_course(request):
    if not request.user.is_teacher:
        return redirect('student_dashboard')

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
            messages.success(request, 'Course uploaded successfully!')
            return redirect('teacher_dashboard')
    else:
        form = CourseForm()
    return render(request, 'core/upload_course.html', {'form': form})


@login_required
def add_lesson_to_course(request, course_id):
    if not request.user.is_teacher:
        return redirect('student_dashboard')

    course = Course.objects.get(id=course_id)

    if request.method == 'POST':
        form = CourseLessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            messages.success(request, 'Lesson added successfully!')
            return redirect('add_lesson', course_id=course.id)
    else:
        form = CourseLessonForm()
    return render(request, 'core/add_lesson.html', {'form': form, 'course': course})


def course_list(request):
    courses = Course.objects.all()
    return render(request, 'core/course_list.html', {'courses': courses})


def course_detail(request, course_id):
    course = Course.objects.get(id=course_id)
    lessons = CourseLesson.objects.filter(course=course)
    return render(request, 'core/course_detail.html', {'course': course, 'lessons': lessons})

@login_required
def course_create(request):
    if not request.user.is_teacher:
        return redirect('student_dashboard')

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
            messages.success(request, "Course created successfully!")
            return redirect('teacher_dashboard')
    else:
        form = CourseForm()

    return render(request, 'core/course_form.html', {'form': form})

from django.shortcuts import redirect

from .models import CourseEnrollment

@login_required
def enroll_course(request, course_id):
    course = Course.objects.get(id=course_id)
    # Prevent duplicate enrollments
    enrollment, created = CourseEnrollment.objects.get_or_create(
        user=request.user, course=course
    )

    if created:
        messages.success(request, "You are now enrolled in this course!")
    else:
        messages.info(request, "You're already enrolled in this course.")

    return redirect('course_detail', course_id=course_id)
