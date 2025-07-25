from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, TeacherProfile
from .models import TeacherProfile, INSTRUMENT_CHOICES, Lesson
from .models import Course, CourseLesson

# forms.py
class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class TeacherProfileForm(forms.ModelForm):
    instruments_taught = forms.MultipleChoiceField(
        choices=INSTRUMENT_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = TeacherProfile
        fields = ['name', 'instruments_taught', 'bio']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Convert comma-separated string to list for initial display
        if self.instance and self.instance.instruments_taught:
            self.initial['instruments_taught'] = [
                i.strip() for i in self.instance.instruments_taught.split(',') 
            ]

    def clean_instruments_taught(self):
        # Join selected instruments into a comma-separated string
        instruments = self.cleaned_data['instruments_taught']
        return ', '.join(instruments)
    



class LessonRequestForm(forms.ModelForm):
    time = forms.TimeField(
        widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        label="Preferred Time"
    )

    class Meta:
        model = Lesson
        fields = ['title', 'description', 'date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class RescheduleLessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['new_date', 'new_time']
        widgets = {
            'new_date': forms.DateInput(attrs={'type': 'date'}),
            'new_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class LessonProgressForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['progress_note']
        widgets = {
            'progress_note': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write progress or feedback...'}),
        }

# forms.py


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'price']

class CourseLessonForm(forms.ModelForm):
    class Meta:
        model = CourseLesson
        fields = ['title', 'description', 'video', 'material', 'youtube_url', 'order']
