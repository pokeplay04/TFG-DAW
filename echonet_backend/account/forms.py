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
        if avatar_file:
            cropped = crop_center_square(avatar_file)
            original_name = avatar_file.name  # ← usa el nombre original del archivo
            user.avatar.save(original_name, cropped, save=False)

        if commit:
            user.save()

        return user