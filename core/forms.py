from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, TeacherProfile

class UserRegisterForm(UserCreationForm):
    is_teacher = forms.BooleanField(required=False, label="Registering as a teacher?")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_teacher']


class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = ['name', 'instruments_taught', 'bio']
