from django import forms
from django.forms.widgets import EmailInput, PasswordInput, TextInput, Textarea
from .models import ClassRoom

class CreateClassromForm(forms.ModelForm):
    subject = forms.CharField(widget=TextInput(attrs={'class': 'form-control','placeholder': 'Enter Subject for Classroom'}))
    description = forms.CharField(widget=Textarea(attrs={'class': 'form-control','placeholder': 'Enter Description for Classroom'}))
    class Meta:
        model = ClassRoom
        fields = ['subject', 'description', 'image']

