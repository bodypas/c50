from .models import User, Post, Comment, Like, Follow, Profile
from django import forms


# form for new post
class PostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, max_length=500, label="Your post")

    class Meta:
        model = Post
        fields = ['content']