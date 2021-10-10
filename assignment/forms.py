from django import forms
from django.forms import fields
from django.forms.widgets import TextInput, Textarea
from .models import Comment, Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # fields = ['subject', 'description', 'image']
        fields = ['description', 'file']


class CommentForm(forms.ModelForm):
    comment = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Write your comment'}))
    class Meta:
        model = Comment
        fields = ['comment',]
