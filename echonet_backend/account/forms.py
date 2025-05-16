from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import SpotifyUser

class ProfileForm(forms.ModelForm):
    class Meta:
        model = SpotifyUser
        fields = ('display_name', 'avatar')
