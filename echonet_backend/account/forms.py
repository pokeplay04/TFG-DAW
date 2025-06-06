import os
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
        avatar_file = self.cleaned_data.get('avatar')

        # Solo guarda si es un archivo nuevo
        if avatar_file and getattr(avatar_file, 'file', None):
            cropped = crop_center_square(avatar_file)
            original_name = os.path.basename(avatar_file.name)
            user.avatar.save(original_name, cropped, save=False)

        if commit:
            user.save()

        return user