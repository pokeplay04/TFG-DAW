from django.forms import ModelForm

from .models import Post, PostAttachment, PostMusicAttachment


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('body', 'is_private',)


class AttachmentForm(ModelForm):
    class Meta:
        model = PostAttachment
        fields = ('image',)

class MusicAttachmentForm(ModelForm):
    class Meta:
        model = PostMusicAttachment
        fields = ('track_id',)