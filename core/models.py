from django.contrib.auth.models import AbstractUser ,User
from django.db import models
from django.contrib.postgres.fields import ArrayField  # only for PostgreSQL
from django.utils import timezone
from django.conf import settings

INSTRUMENT_CHOICES = [
    ('piano', 'Piano'),
    ('guitar', 'Guitar'),
    ('bass', 'Bass'),
    ('drums', 'Drums'),
    ('sax', 'Saxophone'),
    ('violin', 'Violin'),

]
STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('declined', 'Declined'),
    ('cancelled_by_student', 'Cancelled by Student'),
    ('cancelled_by_teacher', 'Cancelled by Teacher'),
    ('reschedule_requested', 'Reschedule Requested'),
]



# Change from ArrayField or simple CharField to:


class User(AbstractUser):
    is_teacher = models.BooleanField(default=False)

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    instruments_taught = models.CharField(max_length=255)

    bio = models.TextField()

    def __str__(self):
        return self.name

class Lesson(models.Model):
    

    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lessons_taught')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lessons_requested')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    progress_note = models.TextField(blank=True, null=True)
    reschedule_requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reschedule_requests')
    new_date = models.DateField(null=True, blank=True)
    new_time = models.TimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.student.username} → {self.teacher.username}"




class Course(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # ✅ ADD THIS LINE
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class CourseLesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video = models.FileField(upload_to='lesson_videos/', blank=True, null=True)
    material = models.FileField(upload_to='lesson_materials/', blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class CourseEnrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)