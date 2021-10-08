from django import forms
from django.forms import fields
from django.forms.widgets import TextInput, Textarea
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # fields = ['subject', 'description', 'image']
        fields = ['description', 'file']

