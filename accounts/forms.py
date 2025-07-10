from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
            ('Attendee', 'Attendee'),
            ('Organizer', 'Organizer'),
       ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Registrati come")

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'role')