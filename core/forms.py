from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, TeacherProfile
from .models import TeacherProfile, INSTRUMENT_CHOICES

class UserRegisterForm(UserCreationForm):
    is_teacher = forms.BooleanField(required=False, label="Registering as a teacher?")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_teacher']

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