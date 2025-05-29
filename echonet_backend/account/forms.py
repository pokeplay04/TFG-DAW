from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import SpotifyUser
from .utils import crop_center_square 

class ProfileForm(forms.ModelForm):
    class Meta:
        model = SpotifyUser
        fields = ('display_name', 'avatar')
    
    def save(self, commit=True):
        user = super().save(commit=False)

        if self.cleaned_data.get('avatar'):
            cropped = crop_center_square(self.cleaned_data['avatar'])
            user.avatar.save(self.cleaned_data['avatar'].name , cropped, save=False)  # guardamos sin commit

        if commit:
            user.save()

        return user