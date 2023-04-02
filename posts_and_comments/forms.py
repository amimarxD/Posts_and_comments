from django import forms
from .models import Post


class PostingForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "description"]